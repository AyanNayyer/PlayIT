from models import db, Song, Album
from werkzeug.security import generate_password_hash
from databasefile import datastore

def initialize_sample_data():
    from app import app
    with app.app_context():
        db.create_all()
        datastore.find_or_create_role(name='admin', description='This is the admin role')
        datastore.find_or_create_role(name='artist', description='This is the artist role')
        datastore.find_or_create_role(name='user', description='This is the user role')
        db.session.commit()

        if not datastore.find_user(email='admin@email.com'):
            datastore.create_user(email='admin@email.com', username= 'admin', password=generate_password_hash('admin'), roles=['admin'])
        db.session.commit()


        albums = [Album(creator_name = "Mohit Chauhan", name = "Rockstar", year = 2011),
                Album(creator_name = "Selena Gomez", name = "When the sun goes down", year = 2011),
                Album(creator_name = "A.R. Rahman", name = "Achcham Yenbadhu", year = 2016),
                Album(creator_name = "Tom Odell", name = "Long Way Down", year = 2013),
                Album(creator_name = "Justin Bieber", name = "Father Of Asahd", year = 2019),
                Album(creator_name = "Randwimps", name = "Your Name", year = 2016),
                Album(creator_name = "Queen", name = "A Night at the Opera", year = 1975),
                Album(creator_name = "Ed Sheeran", name = "Divide", year = 2017),
                Album(creator_name = "Arijit Singh", name = "Aashiqui 2", year = 2013),
                Album(creator_name = "Sonu Nigam", name = "Kal Ho Naa Ho", year = 2003)]
                

        songs = [Song(name= "Kun Faya Kun", creator_name= "Mohit Chauhan", album_id=1, lyrics= 
                    """या निज़ामुद्दीन औलिया
                        या निज़ामुद्दीन सलक़ा

                        कदम बढ़ा ले
                        हदों को मिटा ले
                        आजा ख़ालीपन में पी का घर तेरा
                        तेरे बिन ख़ाली, आजा, ख़ालीपन में
                        तेरे बिन ख़ाली, आजा, ख़ालीपन में

                        रंगरेज़ा
                        रंगरेज़ा
                        रंगरेज़ा

                        كن فيكون، كن فيكون، فيكون
                        فيكون، فيكون، فيكون
                        كن فيكون، كن فيكون، فيكون
                        فيكون، فيكون، فيكون

                        जब कहीं पे कुछ नहीं भी नहीं था
                        वही था, वही था, वही था, वही था
                        जब कहीं पे कुछ नहीं भी नहीं था
                        वही था, वही था, वही था, वही था

                        वो जो मुझ में समाया
                        वो जो तुझ में समाया
                        मौला वही वही माया
                        वो जो मुझ में समाया
                        वो जो तुझ में समाया
                        मौला वही वही माया

                        كن فيكون، كن فيكون
                        صدق الله العلي العظيم

                        रंगरेज़ा रंग मेरा तन, मेरा मन
                        ले ले रंगाई चाहे तन, चाहे मन
                        रंगरेज़ा रंग मेरा तन, मेरा मन
                        ले ले रंगाई चाहे तन, चाहे मन

                        सजरा सवेरा मेरे तन बरसे
                        कजरा अँधेरा तेरी जलती लौ
                        सजरा सवेरा मेरे तन बरसे
                        कजरा अँधेरा तेरी जलती लौ
                        क़तरा मिला जो तेरे दर पर से
                        ओ मौला, मौला

                        كن فيكون، كن فيكون
                        كن فيكون، كن فيكون
                        كن فيكون، كن فيكون، فيكون
                        فيكون، فيكون، فيكون
                        كن فيكون، كن فيكون، فيكون
                        فيكون، فيكون، فيكون

                        जब कहीं पे कुछ नहीं भी नहीं था
                        वही था, वही था, वही था, वही था
                        जब कहीं पे कुछ नहीं भी नहीं था
                        वही था, वही था, वही था, वही था

                        كن فيكون، كن فيكون
                        صدق الله العلي العظيم
                        صدق رسوله النبي الكريم
                        صلّ الله عليه وسلم
                        صلّ الله عليه وسلم

                        ओ मुझपे करम सरकार तेरा
                        अर्ज़ तुझे, "कर दे मुझे मुझसे ही रिहा
                        अब मुझको भी हो दीदार मेरा
                        कर दे मुझे मुझसे ही रिहा
                        मुझसे ही रिहा"

                        मन के मेरे ये भरम
                        कच्चे मेरे ये करम
                        लेके चाले है कहाँ
                        मैं तो जानूँ ही ना

                        तू है मुझमें समाया
                        कहाँ लेके मुझे आया
                        मैं हूँ तुझमें समाया
                        तेरे पीछे चला आया
                        तेरा ही मैं एक साया

                        तूने मुझको बनाया
                        मैं तो जग को ना भाया
                        तुने गले से लगाया
                        हक़ तू ही है ख़ुदाया
                        सच तू ही है ख़ुदाया

                        كن فيكون، كن فيكون، فيكون
                        فيكون، فيكون، فيكون
                        كن فيكون، كن فيكون، فيكون
                        فيكون، فيكون، فيكون

                        जब कहीं पे कुछ नहीं भी नहीं था
                        वही था, वही था, वही था, वही था
                        जब कहीं पे कुछ नहीं भी नहीं था
                        वही था, वही था, वही था, वही था""", genre= 'Bollywood', duration= 381, likes= 11, play_count= 25),
                Song(name= "Who Says", creator_name= "Selena Gomez", album_id=2, lyrics= 
                    """I wouldn't wanna be anybody else, hey
                        You made me insecure
                        Told me I wasn't good enough
                        But who are you to judge?
                        When you're a diamond in the rough
                        I'm sure you got some things
                        You'd like to change about yourself
                        But when it comes to me
                        I wouldn't want to be anybody else
                        Na-na-na-na, na-na-na-na
                        Na-na-na-na, na
                        Na-na-na-na, na-na-na-na
                        Na-na-na-na, na
                        I'm no beauty queen
                        I'm just beautiful me""", genre= 'Pop', duration= 201, likes= 0, play_count= 4), 
                Song(name= "Rasaali", creator_name= "A.R. Rahman", album_id=3, lyrics= 
                    """Male : Parakkum rasaaliye rasaaliye nillu
                        Ingu nee vegama naan vegama sollu
                        Gadigaram poi sollum endre naan kandennn
                        Kizhakellam merkagida.. kandene

                        Female : Paravai pol aaginen pol aaginen indru
                        Siragum en kaigalum en kaigalum ondru

                        Male : Rasaaliiiee.. pandhayama.. pandhayama..
                        Nee mundhiya naan mundhiya paarpom parpomm

                        Mudhalil yaar solvadhu yaar solvadhu anbai
                        Mudhalil yaar eivadhu yaar Eivadhu ambai""", genre= 'Tamil', duration= 330, likes= 9, play_count= 9),
                Song(name= "Another Love", creator_name= "Tom Odell", album_id=4, lyrics= 
                    """I wanna take you somewhere so you know I care
                        But it's so cold, and I don't know where
                        I brought you daffodils in a pretty string
                        But they won't flower like they did last spring
                        And I wanna kiss you, make you feel alright
                        I'm just so tired to share my nights
                        I wanna cry and I wanna love
                        But all my tears have been used up
                        On another love, another love
                        All my tears have been used up
                        On another love, another love
                        All my tears have been used up
                        On another love, another love
                        All my tears have been used up""", genre= 'Indie Rock', duration= 244, likes= 9, play_count= 26),
                Song(name= "No Brainer", creator_name= "Justin Bieber", album_id=5, lyrics= 
                    """We the Best Music!
                        Another one!
                        DJ Khaled!
                        You stick out of the crowd, baby, it's a no-brainer
                        It ain't that hard to choose
                        Him or me, be for real, baby, it's a no-brainer
                        You got your mind unloose
                        Go hard and watch the sun rise
                        One night'll change your whole life
                        Off top, drop-top, baby it's a no-brainer
                        Put 'em up if you with me
                        Yeah, yeah-eah, yeah, yeah-eah-eah
                        In the middle, woah
                        Woah-woah-oah, oh, oh-oh, ooh""", genre= 'Hip Hop', duration= 266, likes= 4, play_count= 9),
                Song(name= "Nandemonaiya", creator_name= "Radwimps", album_id=6, lyrics= 
                    """[Verse 1]
                        Futari no aida toorisugita kaze wa
                        Doko kara sabishisa wo hakondekita no
                        Naitari shita sono ato no sora wa
                        Yake ni sukitootteitari shitanda
                        Itsumo wa togatte tachichi no kotoba ga
                        Kyou wa atatakaku kanjimashita
                        Yasashisa mo egao mo yume no katarikata mo
                        Shiranakute zenbu kimi wo maneta yo

                        [Pre-Chorus]
                        Mou sukoshi dake de ii ato sukoshi dake de ii
                        Mou sukoshi dake de ii kara
                        Mou sukoshi dake de ii ato sukoshi dake de ii
                        Mou sukoshi dake kuttsuiteiyou ka""", genre= 'Japanese', duration= 344, likes= 5, play_count= 7),
                Song(name= "Bohemian Rhapsody", creator_name= "Queen", album_id=7, lyrics= 
                    """Is this the real life? Is this just fantasy?
                        Caught in a landslide, no escape from reality
                        Open your eyes, look up to the skies and see
                        I'm just a poor boy, I need no sympathy
                        Because I'm easy come, easy go, little high, little low
                        Any way the wind blows doesn't really matter to me, to me
                        Mama, just killed a man
                        Put a gun against his head, pulled my trigger, now he's dead
                        Mama, life had just begun
                        But now I've gone and thrown it all away
                        Mama, ooh, didn't mean to make you cry
                        If I'm not back again this time tomorrow
                        Carry on, carry on as if nothing really matters
                        Too late, my time has come
                        Sends shivers down my spine, body's aching all the time
                        Goodbye, everybody, I've got to go
                        Gotta leave you all behind and face the truth
                        Mama, ooh (any way the wind blows)
                        I don't wanna die
                        I sometimes wish I'd never been born at all
                        I see a little silhouetto of a man
                        Scaramouche, Scaramouche, will you do the Fandango?
                        Thunderbolt and lightning, very, very frightening me
                        (Galileo) Galileo, (Galileo) Galileo, Galileo Figaro, magnifico
                        But I'm just a poor boy, nobody loves me
                        He's just a poor boy from a poor family
                        Spare him his life from this monstrosity
                        Easy come, easy go, will you let me go?
                        بِسْمِ ٱللَّٰهِ
                        No, we will not let you go (let him go)
                        بِسْمِ ٱللَّٰهِ
                        We will not let you go (let him go)
                        بِسْمِ ٱللَّٰهِ
                        We will not let you go (let me go)
                        Will not let you go (let me go)
                        Never, never, never, never let me go
                        No, no, no, no, no, no, no
                        Oh, mamma mia, mamma mia
                        Mamma mia, let me go
                        Beelzebub has a devil put aside for me, for me, for me
                        So you think you can stone me and spit in my eye?
                        So you think you can love me and leave me to die?
                        Oh, baby, can't do this to me, baby
                        Just gotta get out, just gotta get right outta here
                        Ooh
                        Ooh, yeah, ooh, yeah
                        Nothing really matters, anyone can see
                        Nothing really matters
                        Nothing really matters to me""", genre= 'Rock', duration= 367, likes= 2, play_count= 2),
                Song(name= "Shape of You", creator_name= "Ed Sheeran", album_id=8, lyrics= 
                    """The club isn't the best place to find a lover
                        So the bar is where I go
                        Me and my friends at the table doing shots
                        Drinking fast and then we talk slow
                        Come over and start up a conversation with just me
                        And trust me I'll give it a chance now
                        Take my hand, stop, put Van the Man on the jukebox
                        And then we start to dance, and now I'm singing like
                        Girl, you know I want your love
                        Your love was handmade for somebody like me
                        Come on now, follow my lead
                        I may be crazy, don't mind me
                        Say, boy, let's not talk too much
                        Grab on my waist and put that body on me
                        Come on now, follow my lead
                        Come, come on now, follow my lead
                        I'm in love with the shape of you
                        We push and pull like a magnet do
                        Although my heart is falling too
                        I'm in love with your body
                        And last night you were in my room
                        And now my bedsheets smell like you
                        Every day discovering something brand new
                        I'm in love with your body
                        (Oh-I-oh-I-oh-I-oh-I)
                        I'm in love with your body
                        (Oh-I-oh-I-oh-I-oh-I)
                        I'm in love with your body
                        (Oh-I-oh-I-oh-I-oh-I)
                        I'm in love with your body
                        Every day discovering something brand new
                        I'm in love with the shape of you
                        """, genre= 'Pop', duration= 234, likes= 7, play_count= 10),
                Song(name= "Tum Hi Ho", creator_name= "Arijit Singh", album_id=9, lyrics= 
                    """हम तेरे बिन अब रह नहीं सकते
                        तेरे बिना क्या वजूद मेरा?
                        हम तेरे बिन अब रह नहीं सकते
                        तेरे बिना क्या वजूद मेरा?
                        तुझ से जुदा अगर हो जाएँगे
                        तो ख़ुद से ही हो जाएँगे जुदा

                        [Chorus]
                        क्योंकि तुम ही हो, अब तुम ही हो
                        ज़िंदगी अब तुम ही हो
                        चैन भी, मेरा दर्द भी
                        मेरी आशिक़ी अब तुम ही हो

                        [Verse 2]
                        तेरा-मेरा रिश्ता है कैसा?
                        एक पल दूर गवारा नहीं
                        तेरे लिए हर रोज़ हैं जीते
                        तुझ को दिया मेरा वक्त सभी
                        कोई लमहा मेरा ना हो तेरे बिना
                        हर साँस पे नाम तेरा""", genre= 'Bollywood', duration= 266, likes= 3, play_count= 4),
                Song(name= "Kal Ho Naa Ho", creator_name= "Sonu Nigam", album_id=10, lyrics= 
                    """Har ghadi badal raha hai roop zindagi
                        Chaav hai kabhi kabhi hai dhoop zindagi
                        Har pal yahan jee bhar jiyo
                        Jo hai sama, kal ho naa ho
                        Har ghadi badal raha hai roop zindagi
                        Chaav hai kabhi kabhi hai dhoop zindagi
                        Har pal yahan jee bhar jiyo
                        Jo hai sama, kal ho naa ho

                        [Verse 1]
                        Chaahe jo tumhe poore dil se
                        Milta hai woh mushkil se
                        Aisa jo koi kahin hai
                        Bas vahi sabse hasin hai
                        Us haath ko tum thaam lo
                        Woh meherbaan kal ho naa ho
                        """, genre= 'Bollywood', duration= 312, likes= 1, play_count= 3)]
                

        for album in albums:
            if not Album.query.filter_by(name= album.name).first():
                db.session.add(album)
                
        for song in songs:
            if not Song.query.filter_by(name= song.name).first():
                db.session.add(song)

        db.session.commit()
            