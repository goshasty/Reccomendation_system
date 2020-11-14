def prefilter_items(data, item_features, take_n_popular=0):
    popularity = data_train.groupby('item_id')['user_id'].nunique().reset_index()
    popularity['user_id'] = popularity['user_id'] / data_train['user_id'].nunique()
    popularity.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    # deleted very popular and unpopular items
    take_n = popularity[(popularity['share_unique_users'] < 0.5) & (popularity['share_unique_users'] > 0.01)]

    if take_n_popular != 0:
        # in case if we would like to reduce our sample we sort items in decending order to keep the most popular one
        take_n = take_n.sort_values('share_unique_users', ascending=False)
        take_n = take_n[:take_n_popular].item_id.tolist()
    else:
        take_n = take_n.item_id.tolist()

    data = data[data['item_id'].isin(take_n)]
    # added additional information about items
    full_data = pd.merge(data, item_features, on='item_id')
    return full_data


def postfilter_items(user_id, recommednations):
    pass

#в связи с тем, что мы в def prefilter_items уменьшили матрицу user-items у нас может не быть некоторых users
def get_similar_items_recommendation(user, model, N=5):
    """Рекомендуем товары, похожие на топ-N купленных юзером товаров"""
    recs = model.similar_items(itemid_to_id[user], N=N)
    all_recs= [id_to_itemid[rec[0]] for rec in recs]
    return  all_recs

def get_similar_users_recommendation(user, model, N=5):
    """Рекомендуем топ-N товаров, среди купленных похожими юзерами"""
    try:
        res = [id_to_itemid[rec[0]] for rec in model.recommend(userid=userid_to_id[user],
                                        user_items=csr_matrix(user_item_matrix).tocsr(),   # на вход user-item matrix
                                        N=N,
                                        filter_already_liked_items=False,
                                        #filter_items=[itemid_to_id[999999]],  # !!! have already deleted in def prefilter_items
                                        recalculate_user=True)]
    except KeyError:
        res = None

    return res

