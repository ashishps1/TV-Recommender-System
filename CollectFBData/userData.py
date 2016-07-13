import fbGraphAPI
import auth
import json
import passlib


class UserData:

    def hashUser(self,userId):
        hashedUser = sha256_crypt.encrypt(userId)
        return hashedUser

    def writeString(self, dict, key, label, outFile):
    	val = ""
    	if(key in dict):
    		val = dict[key]

    	if(val == None or len(val) == 0):
    		val = "N/A"

    	output.write("\t\t<%s>%s</%s>\n" % (label, escape(val.encode('utf-8')), label))
        print "\t\t<%s>%s</%s>\n" % (label, escape(val.encode('utf-8')), label)

    def writeString2(self, dict, key, subkey, label, outFile):
        vals = []
        if(key in dict):
        	for item in dict[key]:
        		vals.append(item[subkey])
        val = ",".join(vals)
        if(len(val) == 0):
            val = "N/A"

        output.write("\t\t<%s>%s</%s>\n" % (label, escape(val.encode('utf-8')), label))
        print "\t\t<%s>%s</%s>\n" % (label, escape(val.encode('utf-8')), label)

    def main(self):
    	graph = fbGraphAPI.GraphAPI(auth.get_token())
    	myFriends = graph.get_connections("me", "friends")
        outFile = open("friendData.json", "w+")
        print '{\n\tusers : {\n'
        outFile.write('{ users : {\n')

            # Loop through all my friends
    	for friend in friends['data']:
            # Create a one-way hash of the Facebook user ID to anonymize the data
            print "\tuser id:\"%s\">\n" % (oneWayHash(friend["id"]))
            outFile.write("\tuser id:\"%s\">\n" % (oneWayHash(friend["id"])))

            # Retrieve the friend's user object to get information such as gender, locale, etc...
            friendProfileInfo = graphApi.get_object(friend["id"])

            writeStringJSON(friendProfileInfo, "gender", "gender", outFile)
            writeStringJSON(friendProfileInfo, "locale", "locale", outFile)
            writeStringJSON2(friendProfileInfo, "favorite_athletes", "name", "athletes", outFile)
            writeStringJSON2(friendProfileInfo, "favorite_teams", "name", "teams", outFile)
            # Perform a FQL query to retrieve relevant data on what interests each person...
            result = graphApi.fql("SELECT about_me, activities, interests, music, movies, tv, books, quotes, sports FROM user WHERE uid = %s" % (friend['id']))
            # Somewhat valid assumption that FB UID's are, indeed, unique, and that FB doesn't lie...
            userInterests = result[0]
            writeStringJSON(userInterests, "about_me", "about", outFile)
            writeStringJSON(userInterests, "tv", "tv", outFile)
            writeStringJSON(userInterests, "movies", "movies", outFile)
            writeStringJSON(userInterests, "music", "music", outFile)
            writeStringJSON(userInterests, "books", "books", outFile)
            writeStringJSON(userInterests, "interests", "interests", outFile)
            writeStringJSON2(userInterests, "sports", "name", "sports", outFile)

    	outFile.write("\n\t}\n}")
        print "\n\t}\n}"

Data = UserData()
Data.main()
