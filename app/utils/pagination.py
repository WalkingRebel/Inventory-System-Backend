def paginate(query, page=1, limit=10):
    return query.offset((page - 1) * limit).limit(limit).all()
