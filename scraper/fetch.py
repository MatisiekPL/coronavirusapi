from github import Github, UnknownObjectException

g = Github()
repo = g.get_repo("CSSEGISandData/COVID-19")
for commit in repo.get_commits():
    try:
        contents = repo.get_contents('archived_data/data/bnonews_data.txt', ref=commit.sha)
        with open("coronavirus-"+commit.sha[0:8]+".txt", "wb") as text_file:
            text_file.write(contents.decoded_content)
    except UnknownObjectException:
        print('err')