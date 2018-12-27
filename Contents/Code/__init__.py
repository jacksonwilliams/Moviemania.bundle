import requests

def Start():
    HTTP.CacheTime = 0


class MoviemaniaAgentMovies(Agent.Movies):
    name = 'Moviemania'
    languages = [Locale.Language.NoLanguage]
    primary_provider = False
    contributes_to = [
		'com.plexapp.agents.imdb',
		'com.plexapp.agents.themoviedb'
	]

    def search(self, results, media, lang):
        if media.primary_metadata:
			results.Append(MetadataSearchResult(
				id = media.primary_metadata.id,
				score = 100
			))

    def update(self, metadata, media, lang):
        valid_names = list()

        try:
            json_obj = requests.get('https://www.moviemania.io/plex/posters?type=movie&id=%s' % metadata.id).json()
        except:
            json_obj = None
       
        if json_obj:
            for index, poster in enumerate(json_obj['posters']):
                valid_names.append(poster['large'])
                metadata.posters[poster['large']] = Proxy.Preview(requests.get(poster['preview']).content, sort_order=index+1)

        metadata.posters.validate_keys(valid_names)


class MoviemaniaAgentTVShows(Agent.TV_Shows):
	name = 'Moviemania'
	languages = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to = [
		'com.plexapp.agents.thetvdb',
		'com.plexapp.agents.themoviedb'
	]

	def search(self, results, media, lang):
		if media.primary_agent == 'com.plexapp.agents.thetvdb':
			results.Append(MetadataSearchResult(
				id = media.primary_metadata.id,
				score = 100
			))

		elif media.primary_agent == 'com.plexapp.agents.themoviedb':
			tvdb_id = Core.messaging.call_external_function(
				'com.plexapp.agents.themoviedb',
				'MessageKit:GetTvdbId',
				kwargs = dict(
					tmdb_id = media.primary_metadata.id
				)
			)

			if tvdb_id:
				results.Append(MetadataSearchResult(
					id = tvdb_id,
					score = 100
				))

	def update(self, metadata, media, lang):
		valid_names = list()

		try:
			json_obj = requests.get('https://www.moviemania.io/plex/posters?type=tv&id=%s' % metadata.id).json()
		except:
			json_obj = None

		if json_obj:
			for index, poster in enumerate(json_obj['posters']):
				valid_names.append(poster['large'])
				metadata.posters[poster['large']] = Proxy.Preview(requests.get(poster['preview']).content, sort_order=index+1)

		metadata.posters.validate_keys(valid_names)
