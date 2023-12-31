from app.schemas.user_schema import UserMetaDataSchema


def convert_dict_to_model(data_dict)->UserMetaDataSchema:
    model_data = {
        "username": data_dict["Username"],
        "name": data_dict["Name"],
        "commits": int(data_dict["Commits"]),
        "stars": int(data_dict["Stars"]),
        "forks": int(data_dict["Forks"]),
        "lines_code": int(data_dict["Code Lines"]),
        "lines_tests": int(data_dict["Tests"]),
        "followers": int(data_dict["Followers"]),
        "following": int(data_dict["Following"]),
        "public_repos": int(data_dict["Public Repos"]),
        "empty_repos": int(data_dict["Empty Repositories"]),
        "forked_repos": int(data_dict["Forked Repositories"]),
    }
    return UserMetaDataSchema(**model_data)