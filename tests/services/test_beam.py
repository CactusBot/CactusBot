from cactusbot.packets import MessagePacket
from cactusbot.services.beam.parser import BeamParser


def test_parse_message():

    assert BeamParser.parse_message({
        'channel': 2151,
        'id': '7f43cca0-a9c5-11e6-9c8f-6bd6b629c2eb',
        'message': {
            'message': [
                {'data': 'Hello, world!',
                 'text': 'Hello, world!',
                 'type': 'text'}
            ],
            'meta': {}
        },
        'user_id': 2547,
        'user_name': '2Cubed',
        'user_roles': ['Owner']
    }).json == {
        "message": [{
            "type": "text",
            "data": "Hello, world!",
            "text": "Hello, world!"
        }],
        "user": "2Cubed",
        "role": 100,
        "action": False,
        "target": None
    }

    assert BeamParser.parse_message({
        'channel': 2151,
        'id': '8ef6a160-a9c8-11e6-9c8f-6bd6b629c2eb',
        'message': {
            'message': [
                {'data': 'waves ',
                 'text': 'waves ',
                 'type': 'text'},
                {'coords': {'height': 24, 'width': 24, 'x': 72, 'y': 0},
                 'pack': 'default',
                 'source': 'builtin',
                 'text': ':D',
                 'type': 'emoticon'}],
            'meta': {'me': True}},
        'user_id': 95845,
        'user_name': 'Stanley',
        'user_roles': ['User']
    }).json == {
        "message": [{
            "type": "text",
            "data": "waves ",
            "text": "waves "
        }, {
            "type": "emoji",
            "data": "😃",
            "text": ":D"
        }],
        "user": "Stanley",
        "role": 1,
        "action": True,
        "target": None
    }


def test_parse_follow():

    assert BeamParser.parse_follow({
        'following': True,
        'user': {
            'avatarUrl': 'https://uploads.beam.pro/avatar/l0icubxz-95845.jpg',
            'bio': None,
            'channel': {'audience': 'teen',
                        'badgeId': None,
                        'coverId': None,
                        'createdAt': '2016-03-05T20:41:21.000Z',
                        'deletedAt': None,
                        'description': None,
                        'featured': False,
                        'ftl': 0,
                        'hasTranscodes': True,
                        'hasVod': False,
                        'hosteeId': None,
                        'id': 68762,
                        'interactive': False,
                        'interactiveGameId': None,
                        'languageId': None,
                        'name': "Stanley's Channel",
                        'numFollowers': 0,
                        'online': False,
                        'partnered': False,
                        'suspended': False,
                        'thumbnailId': None,
                        'token': 'Stanley',
                        'transcodingProfileId': None,
                        'typeId': None,
                        'updatedAt': '2016-08-16T02:53:01.000Z',
                        'userId': 95845,
                        'viewersCurrent': 0,
                        'viewersTotal': 0,
                        'vodsEnabled': True},
            'createdAt': '2016-03-05T20:41:21.000Z',
            'deletedAt': None,
            'experience': 401,
            'frontendVersion': None,
            'id': 95845,
            'level': 13,
            'primaryTeam': None,
            'social': {'verified': []},
            'sparks': 2236,
            'updatedAt': '2016-08-20T04:35:25.000Z',
            'username': 'Stanley',
            'verified': True
        }
    }).json == {
        "user": "Stanley",
        "event": "follow",
        "success": True
    }

    assert BeamParser.parse_follow({
        'following': False,
        'user': {
            'avatarUrl': 'https://uploads.beam.pro/avatar/l0icubxz-95845.jpg',
            'bio': None,
            'channel': {'audience': 'teen',
                        'badgeId': None,
                        'coverId': None,
                        'createdAt': '2016-03-05T20:41:21.000Z',
                        'deletedAt': None,
                        'description': None,
                        'featured': False,
                        'ftl': 0,
                        'hasTranscodes': True,
                        'hasVod': False,
                        'hosteeId': None,
                        'id': 68762,
                        'interactive': False,
                        'interactiveGameId': None,
                        'languageId': None,
                        'name': "Stanley's Channel",
                        'numFollowers': 0,
                        'online': False,
                        'partnered': False,
                        'suspended': False,
                        'thumbnailId': None,
                        'token': 'Stanley',
                        'transcodingProfileId': None,
                        'typeId': None,
                        'updatedAt': '2016-08-16T02:53:01.000Z',
                        'userId': 95845,
                        'viewersCurrent': 0,
                        'viewersTotal': 0,
                        'vodsEnabled': True},
            'createdAt': '2016-03-05T20:41:21.000Z',
            'deletedAt': None,
            'experience': 401,
            'frontendVersion': None,
            'id': 95845,
            'level': 13,
            'primaryTeam': None,
            'social': {'verified': []},
            'sparks': 2236,
            'updatedAt': '2016-08-20T04:35:25.000Z',
            'username': 'Stanley',
            'verified': True
        }
    }).json == {
        "user": "Stanley",
        "event": "follow",
        "success": False
    }


def test_parse_subscribe():

    assert BeamParser.parse_subscribe({
        'user': {
            'avatarUrl': 'https://uploads.beam.pro/avatar/20621.jpg',
            'bio': 'Broadcasting Daily at 10 AM PST. Join in on fun with mostly Minecraft.',
            'createdAt': '2015-05-06T05:13:52.000Z',
            'deletedAt': None,
            'experience': 97980,
            'frontendVersion': None,
            'id': 20621,
            'level': 88,
            'primaryTeam': 89,
            'social': {
                'player': 'https://player.me/innectic',
                'twitter': 'https://twitter.com/Innectic',
                'verified': []
            },
            'sparks': 174519,
            'updatedAt': '2016-08-27T02:11:24.000Z',
            'username': 'Innectic',
            'verified': True
        }
    }).json == {
        "user": "Innectic",
        "event": "subscribe",
        "success": True
    }


def test_parse_host():

    assert BeamParser.parse_host({
        'hoster': {
            'audience': 'teen',
            'badgeId': None,
            'coverId': None,
            'createdAt': '2016-03-05T20:41:21.000Z',
            'deletedAt': None,
            'description': None,
            'featured': False,
            'ftl': 0,
            'hasTranscodes': True,
            'hasVod': False,
            'hosteeId': 3016,
            'id': 68762,
            'interactive': False,
            'interactiveGameId': None,
            'languageId': None,
            'name': "Stanley's Channel",
            'numFollowers': 0,
            'online': False,
            'partnered': False,
            'suspended': False,
            'thumbnailId': None,
            'token': 'Stanley',
            'transcodingProfileId': None,
            'typeId': None,
            'updatedAt': '2016-11-13T20:21:59.000Z',
            'userId': 95845,
            'viewersCurrent': 0,
            'viewersTotal': 0,
            'vodsEnabled': True},
        'hosterId': 68762
    }).json == {
        "user": "Stanley",
        "event": "host",
        "success": True
    }


def test_synthesize():

    assert BeamParser.synthesize(MessagePacket(
        "Hey, ",
        ("tag", "Stanley"),
        "! ",
        ("emoji", "🌵"),
        " Check out ",
        ("link", "https://cactusbot.rtfd.org", "cactusbot.rtfd.org"),
        "!"
    )) == (("Hey, @Stanley! :cactus Check out cactusbot.rtfd.org!",), {})

    assert BeamParser.synthesize(MessagePacket(
        "waves", action=True
    )) == (("/me waves",), {})

    assert BeamParser.synthesize(MessagePacket(
        "Hello!", target="Stanley"
    )) == (("Stanley", "Hello!",), {"method": "whisper"})
