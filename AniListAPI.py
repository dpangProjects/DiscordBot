import requests
import json5

class AniListAPI:

    def __init__(self):
        return

    def getinfo(title):
        # Here we define our query as a multi-line string
        query = '''
        query ($search: String, $name: String) { # Define which variables will be used in the query (id)
          Media (search: $search, format: MANGA) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title{
                romaji
                english 
            }
            coverImage{
                large
            }
          }
          User (name: $name){
            name
            statistics{
                manga{
                    scores{
                        score
                        mediaIds
                    }
                }
            }    
          }
        }
        '''

        # Define our query variables and values that will be used in the query request
        variables = {
            'name': "KnowName",
            'search': title
        }

        url = 'https://graphql.anilist.co'

        # Make the HTTP Api request
        response = requests.post(url, json={'query': query, 'variables': variables})

        # use response.text to get the string of what you wanted, then json.loads to convert to string
        info = json5.loads(response.text)  # info is a dict, ex) info['data']['Media']['title']['native'] to get japanese

        title = info['data']['Media']['title']['romaji']
        image = info['data']['Media']['coverImage']['large']
        scores = info['data']['User']['statistics']['manga']['scores']
        goal_id = info['data']['Media']['id']
        goal_score = 0

        for i in range(len(scores)):
            score = scores[i]['score']
            for Id in scores[i]['mediaIds']:
                if Id == goal_id:
                    goal_score = score

        print(title)
        print(goal_id)
        return title, goal_score, image


