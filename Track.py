class Track(object):
    def __init__ (self, name, id):
        self.name = name
        self.id = id
        self.acousticness = None
        self.danceability = None
        self.energy = None
        self.instrumentalness = None
        self.key = None
        self.liveness = None
        self.loudness = None
        self.mode = None
        self.speechiness = None
        self.tempo = None
        self.time_signature = None
        self.valence = None

    def set_all_features(self, features):
        self.acousticness = features['acousticness']
        self.danceability = features['danceability']
        self.energy = features['energy']
        self.instrumentalness = features['instrumentalness']
        self.key = features['key']
        self.liveness = features['liveness']
        self.loudness = features['loudness']
        self.mode = features['mode']
        self.speechiness = features['speechiness']
        self.tempo = features['tempo']
        self.time_signature = features['time_signature']
        self.valence = features['valence']

    def get_all_features(self):
        return [self.acousticness, self.danceability, self.energy, self.instrumentalness, self.key, self.liveness,
        self.loudness, self.mode, self.speechiness, self.tempo, self.time_signature, self.valence]

    def has_features_check(self):
        features = self.get_all_features()
        for feature in features:
            if feature == None:
                return False
        return True

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        return [self.name, self.id, self.get_all_features()] == [other.name, other.id, other.get_all_features()]
