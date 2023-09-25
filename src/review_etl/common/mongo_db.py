def get_connect_string(username: str, password: str) -> str:
    return (
        f"mongodb+srv://{username}:{password}"
        f"@test-cluster.elfmjz1.mongodb.net/?retryWrites=true&w=majority"
    )


def create_collection_if_not_exists(col_name, db):
    if col_name not in db.list_collection_names():
        return db.create_collection(col_name)


def get_non_matching_records_pipe(
    foreign_table, local_field, foreign_field, limit=None
):
    stage_lookup = {
        "$lookup": {
            "from": foreign_table,
            "localField": local_field,
            "foreignField": foreign_field,
            "as": "joined",
        }
    }
    stage_match = {"$match": {"joined": []}}
    if limit:
        stage_limit = {"$limit": limit}
        return [stage_lookup, stage_match, stage_limit]
    else:
        return [stage_lookup, stage_match]