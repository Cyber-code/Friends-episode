import rumps
from friends_data import FriendsEpisode
rumps.debug_mode(True)
class friendsApp(rumps.App):
    @rumps.clicked('Get a Friends Episode')
    def button(self, sender):
        f = FriendsEpisode()
        data = f.get_info()
        print(data)
        window = rumps.Window("Friends")
        window.title = data["title"] + 'Friends episode s{:02d}e{:02d}'.format(data["saison_episode"][0],data["saison_episode"][1])
        window.message = data["date"]
        window.default_text = data["synopsis"]
        window.icon = data["file"].name
        window.dimensions = (560,560)

        window.add_buttons('See on Netflix',)

        response = window.run()
        print(response)

        if response.clicked == 2:
            f.netflix()
        

if __name__ == "__main__":
    friendsApp("Friends").run()