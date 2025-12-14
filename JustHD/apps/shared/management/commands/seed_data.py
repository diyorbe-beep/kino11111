from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.movies.models import Category, Genre, Movie
from apps.users.models import User
from apps.ratings.models import Rating
from apps.comments.models import Comment

class Command(BaseCommand):
    help = 'Seed database with initial data for JustHD'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        clear = options['clear']

        self.stdout.write(self.style.SUCCESS('🎬 JustHD Database Seeding'))

        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Rating.objects.all().delete()
            Comment.objects.all().delete()
            Movie.objects.all().delete()
            Genre.objects.all().delete()
            Category.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared'))

        self.stdout.write('📚 Creating categories...')
        categories_data = [
            {
                'name': 'Movies',
                'name_uz': 'Filmlar',
                'name_ru': 'Фильмы',
                'description': 'Feature films and movies',
                'description_uz': 'Badiiy filmlar va kinolar',
                'description_ru': 'Художественные фильмы и кино',
                'order': 1,
                'is_active': True,
            },
            {
                'name': 'TV Shows',
                'name_uz': 'TV Dasturlar',
                'name_ru': 'ТВ Шоу',
                'description': 'Television series and shows',
                'description_uz': 'Televizion seriallar va shoular',
                'description_ru': 'Телевизионные сериалы и шоу',
                'order': 2,
                'is_active': True,
            },
            {
                'name': 'Cartoons',
                'name_uz': 'Multfilmlar',
                'name_ru': 'Мультфильмы',
                'description': 'Animated cartoons and anime',
                'description_uz': 'Animatsion multfilmlar va anime',
                'description_ru': 'Анимационные мультфильмы и аниме',
                'order': 3,
                'is_active': True,
            },
            {
                'name': 'Documentaries',
                'name_uz': 'Hujjatli Filmlar',
                'name_ru': 'Документальные фильмы',
                'description': 'Documentary films and educational content',
                'description_uz': 'Hujjatli filmlar va o‘quv materiallari',
                'description_ru': 'Документальные фильмы и обучающий контент',
                'order': 4,
                'is_active': True,
            },
            {
                'name': 'Premier',
                'name_uz': 'Premyera',
                'name_ru': 'Премьера',
                'description': 'Newly released movies and shows',
                'description_uz': 'Yangi chiqqan filmlar va shoular',
                'description_ru': 'Новые фильмы и шоу',
                'order': 5,
                'is_active': True,
            },
        ]

        created_categories = 0
        for data in categories_data:
            category, created = Category.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                created_categories += 1
                self.stdout.write(f'Created: {data["name"]}')
            else:
                for field, value in data.items():
                    setattr(category, field, value)
                category.save()
                self.stdout.write(f'Updated: {data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'Categories: {created_categories}'))

        self.stdout.write('🎭 Creating genres...')
        genres_data = [
            {'name': 'Action', 'name_uz': 'Jangari', 'name_ru': 'Боевик'},
            {'name': 'Adventure', 'name_uz': 'Sarguzasht', 'name_ru': 'Приключения'},
            {'name': 'Sci-Fi', 'name_uz': 'Ilmiy Fantastika', 'name_ru': 'Научная фантастика'},
            {'name': 'Fantasy', 'name_uz': 'Fantastika', 'name_ru': 'Фэнтези'},
            {'name': 'Drama', 'name_uz': 'Drama', 'name_ru': 'Драма'},
            {'name': 'Romance', 'name_uz': 'Romantika', 'name_ru': 'Романтика'},
            {'name': 'Comedy', 'name_uz': 'Komediya', 'name_ru': 'Комедия'},
            {'name': 'Horror', 'name_uz': 'Qo‘rqinchli', 'name_ru': 'Ужасы'},
            {'name': 'Thriller', 'name_uz': 'Triller', 'name_ru': 'Триллер'},
            {'name': 'Mystery', 'name_uz': 'Sir', 'name_ru': 'Мистика'},
            {'name': 'Crime', 'name_uz': 'Jinoyat', 'name_ru': 'Криминал'},
            {'name': 'Biography', 'name_uz': 'Biografiya', 'name_ru': 'Биография'},
            {'name': 'History', 'name_uz': 'Tarix', 'name_ru': 'История'},
            {'name': 'War', 'name_uz': 'Urush', 'name_ru': 'Война'},
            {'name': 'Musical', 'name_uz': 'Musiqiy', 'name_ru': 'Мюзикл'},
            {'name': 'Family', 'name_uz': 'Oila', 'name_ru': 'Семейный'},
            {'name': 'Animation', 'name_uz': 'Animatsion', 'name_ru': 'Анимация'},
            {'name': 'Documentary', 'name_uz': 'Hujjatli', 'name_ru': 'Документальный'},
        ]

        created_genres = 0
        for data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                created_genres += 1
                self.stdout.write(f'Created: {data["name"]}')
            else:
                for field, value in data.items():
                    setattr(genre, field, value)
                genre.save()
                self.stdout.write(f'Updated: {data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'Genres: {created_genres}'))

        self.stdout.write('🎥 Creating movies...')
        action_genre = Genre.objects.get(name='Action')
        scifi_genre = Genre.objects.get(name='Sci-Fi')
        adventure_genre = Genre.objects.get(name='Adventure')
        thriller_genre = Genre.objects.get(name='Thriller')
        fantasy_genre = Genre.objects.get(name='Fantasy')
        comedy_genre = Genre.objects.get(name='Comedy')
        romance_genre = Genre.objects.get(name='Romance')
        drama_genre = Genre.objects.get(name='Drama')
        horror_genre = Genre.objects.get(name='Horror')
        crime_genre = Genre.objects.get(name='Crime')
        animation_genre = Genre.objects.get(name='Animation')
        documentary_genre = Genre.objects.get(name='Documentary')

        movies_category = Category.objects.get(name='Movies')
        tv_category = Category.objects.get(name='TV Shows')
        cartoon_category = Category.objects.get(name='Cartoons')
        documentary_category = Category.objects.get(name='Documentaries')
        premier_category = Category.objects.get(name='Premier')

        movies_data = [
            {
                'title': 'Iron Man',
                'title_uz': 'Temir odam',
                'title_ru': 'Железный человек',
                'description': 'Tony Stark builds a powered suit of armor to fight evil',
                'description_uz': 'Tony Stark yovuzlikka qarshi kurashish uchun qurollangan zirh kostyumi yasaydi',
                'description_ru': 'Тони Старк строит силовой костюм брони для борьбы со злом',
                'release_year': 2008,
                'duration': 126,
                'is_premium': True,
                'content_type': 'movie',
                'genres': [action_genre, scifi_genre, adventure_genre],
                'categories': [movies_category],
            },
            {
                'title': 'Captain America: The Winter Soldier',
                'title_uz': 'Kapiton Amerika: Qish askari',
                'title_ru': 'Капитан Америка: Зимний солдат',
                'description': 'Captain America fights a mysterious assassin known as the Winter Soldier',
                'description_uz': 'Kapiton Amerika Qish askari deb nomlangan sirli suiqasdchi bilan kurashadi',
                'description_ru': 'Капитан Америка сражается с загадочным убийцей, известным как Зимний солдат',
                'release_year': 2014,
                'duration': 136,
                'is_premium': True,
                'content_type': 'movie',
                'genres': [action_genre, scifi_genre, thriller_genre],
                'categories': [movies_category],
            },
            {
                'title': 'The Avengers',
                'title_uz': 'Qasoskorlar',
                'title_ru': 'Мстители',
                'description': 'Earth\'s mightiest heroes must come together to fight Loki',
                'description_uz': 'Yerning eng kuchli qahramonlari Loki ga qarshi kurashish uchun birlashishi kerak',
                'description_ru': 'Могущественные герои Земли должны объединиться, чтобы сразиться с Локи',
                'release_year': 2012,
                'duration': 143,
                'is_premium': False,
                'content_type': 'movie',
                'genres': [action_genre, scifi_genre, fantasy_genre],
                'categories': [movies_category],
            },
            {
                'title': 'Doctor Strange',
                'title_uz': 'Doktor Strange',
                'title_ru': 'Доктор Стрэндж',
                'description': 'A former neurosurgeon embarks on a journey of healing and discovers magic',
                'description_uz': 'Sobiq neyroxirurg shifokorlik safariqa chiqadi va sehrni kashf etadi',
                'description_ru': 'Бывший нейрохирург отправляется в путешествие исцеления и открывает магию',
                'release_year': 2016,
                'duration': 115,
                'is_premium': False,
                'content_type': 'movie',
                'genres': [fantasy_genre, scifi_genre, action_genre],
                'categories': [movies_category],
            },
            {
                'title': 'Breaking Bad',
                'title_uz': 'Breaking Bad',
                'title_ru': 'Во все тяжкие',
                'description': 'A high school chemistry teacher diagnosed with cancer turns to manufacturing drugs',
                'description_uz': 'Rak kasalligi bilan og\'rigan o\'rta maktab kimyo o\'qituvchisi giyohvand moddalar ishlab chiqarishga murojaat qiladi',
                'description_ru': 'Учитель химии средней школы, у которого диагностировали рак, обращается к производству наркотиков',
                'release_year': 2008,
                'duration': 49,
                'is_premium': True,
                'content_type': 'tv_show',
                'genres': [drama_genre, crime_genre, thriller_genre],
                'categories': [tv_category],
            },
            {
                'title': 'The Lion King',
                'title_uz': 'Sherlar qiroli',
                'title_ru': 'Король лев',
                'description': 'Lion cub Simba struggles to accept the responsibilities of adulthood',
                'description_uz': 'Sher bola Simba kattalik mas\'uliyatini qabul qilish uchun kurashadi',
                'description_ru': 'Детеныш льва Симба изо всех сил пытается принять ответственность взрослой жизни',
                'release_year': 1994,
                'duration': 88,
                'is_premium': False,
                'content_type': 'cartoon',
                'genres': [animation_genre, adventure_genre, drama_genre],
                'categories': [cartoon_category],
            },
            {
                'title': 'Planet Earth',
                'title_uz': 'Yer sayyorasi',
                'title_ru': 'Планета Земля',
                'description': 'A documentary series on the wildlife found on Earth',
                'description_uz': 'Yerdagi yovvoyi tabiat haqidagi hujjatli serial',
                'description_ru': 'Документальный сериал о дикой природе на Земле',
                'release_year': 2006,
                'duration': 50,
                'is_premium': False,
                'content_type': 'documentary',
                'genres': [documentary_genre],
                'categories': [documentary_category],
            },
            {
                'title': 'Premier Movie 2024',
                'title_uz': 'Premyera filmi 2024',
                'title_ru': 'Премьера фильма 2024',
                'description': 'Newly released premier movie for 2024',
                'description_uz': '2024 yil uchun yangi chiqqan premyera filmi',
                'description_ru': 'Новый премьерный фильм для 2024 года',
                'release_year': 2024,
                'duration': 120,
                'is_premium': True,
                'is_premier': True,
                'premier_date': timezone.now() - timedelta(days=7),
                'content_type': 'movie',
                'genres': [action_genre, adventure_genre],
                'categories': [premier_category, movies_category],
            },
            # Yangi drama filmlar qo'shamiz
            {
                'title': 'The Shawshank Redemption',
                'title_uz': 'Shawshank qutqarilishi',
                'title_ru': 'Побег из Шоушенка',
                'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency',
                'description_uz': 'Qamalgan ikki erkak bir necha yil davomida bog\'lanib, oddiy odob orqali tasalli va oxir-oqibat qutqarilishni topadilar',
                'description_ru': 'Двое заключенных сближаются за несколько лет, находя утешение и окончательное искупление через акты общей порядочности',
                'release_year': 1994,
                'duration': 142,
                'is_premium': False,
                'content_type': 'movie',
                'genres': [drama_genre],
                'categories': [movies_category],
            },
            {
                'title': 'Forrest Gump',
                'title_uz': 'Forrest Gump',
                'title_ru': 'Форрест Гамп',
                'description': 'The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold through the perspective of an Alabama man with an IQ of 75',
                'description_uz': 'Kennedi va Jonson prezidentliklari, Vetnam voqealari, Uotergeyt va boshqa tarixiy voqealar 75 IQ ga ega Alabama erkak nuqtai nazaridan ochiladi',
                'description_ru': 'Президентства Кеннеди и Джонсона, события Вьетнама, Уотергейт и другие исторические события разворачиваются с точки зрения жителя Алабамы с IQ 75',
                'release_year': 1994,
                'duration': 142,
                'is_premium': False,
                'content_type': 'movie',
                'genres': [drama_genre, romance_genre],
                'categories': [movies_category],
            },
            {
                'title': 'The Godfather',
                'title_uz': 'Xudo otasi',
                'title_ru': 'Крестный отец',
                'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son',
                'description_uz': 'Tashkil etilgan jinoyat sulolasining qarigan patriarxi o\'zining maxfiy imperiyasini boshqarishni istamay turgan o\'g\'liga o\'tkazadi',
                'description_ru': 'Стареющий патриарх организованной преступной династии передает контроль над своей тайной империей своему неохотному сыну',
                'release_year': 1972,
                'duration': 175,
                'is_premium': True,
                'content_type': 'movie',
                'genres': [drama_genre, crime_genre],
                'categories': [movies_category],
            },
        ]

        created_movies = 0
        for data in movies_data:
            try:
                movie_data = {
                    'release_year': data['release_year'],
                    'duration': data['duration'],
                    'is_premium': data['is_premium'],
                    'is_active': True,
                    'content_type': data['content_type'],
                }

                if 'is_premier' in data:
                    movie_data['is_premier'] = data['is_premier']
                if 'premier_date' in data:
                    movie_data['premier_date'] = data['premier_date']

                for field in ['title', 'title_uz', 'title_ru', 'description', 'description_uz', 'description_ru']:
                    if field in data:
                        movie_data[field] = data[field]

                movie, created = Movie.objects.get_or_create(
                    title=data['title'],
                    release_year=data['release_year'],
                    defaults=movie_data
                )

                if created:
                    for genre in data['genres']:
                        movie.genres.add(genre)
                    for category in data['categories']:
                        movie.categories.add(category)
                    created_movies += 1
                    self.stdout.write(f'Created: {data["title"]}')
                else:
                    for field, value in movie_data.items():
                        setattr(movie, field, value)
                    movie.save()

                    movie.genres.clear()
                    for genre in data['genres']:
                        movie.genres.add(genre)

                    movie.categories.clear()
                    for category in data['categories']:
                        movie.categories.add(category)

                    self.stdout.write(f'Updated: {data["title"]}')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating movie "{data["title"]}": {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Movies: {created_movies}'))

        self.stdout.write('👥 Creating users...')
        users_data = [
            {
                'username': 'premium_user',
                'email': 'premium@justhd.com',
                'password': 'Premium123!',
                'first_name': 'Premium',
                'last_name': 'User',
                'is_premium': True,
                'premium_until': timezone.now() + timedelta(days=365)
            },
            {
                'username': 'test_user',
                'email': 'test@justhd.com',
                'password': 'Test123!',
                'first_name': 'Test',
                'last_name': 'User',
                'is_premium': False
            },
        ]

        created_users = 0
        for data in users_data:
            try:
                user, created = User.objects.get_or_create(
                    username=data['username'],
                    defaults={
                        'email': data['email'],
                        'first_name': data['first_name'],
                        'last_name': data['last_name'],
                        'is_premium': data.get('is_premium', False),
                        'premium_until': data.get('premium_until')
                    }
                )

                if created:
                    user.set_password(data['password'])
                    user.save()
                    created_users += 1
                    self.stdout.write(f'Created user: {user.username}')
                else:
                    self.stdout.write(f'User exists: {user.username}')

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user "{data["username"]}": {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'Users: {created_users}'))

        self.stdout.write('⭐ Creating ratings...')
        users = User.objects.all()[:2]
        movies = Movie.objects.all()[:4]

        created_ratings = 0
        for user in users:
            for movie in movies:
                try:
                    rating, created = Rating.objects.get_or_create(
                        user=user,
                        movie=movie,
                        defaults={
                            'score': 8,
                            'comment': f'Great movie! I loved {movie.title}'
                        }
                    )
                    if created:
                        created_ratings += 1
                except Exception as e:
                    pass

        self.stdout.write(self.style.SUCCESS(f'Ratings: {created_ratings}'))

        self.stdout.write('💬 Creating comments...')
        created_comments = 0
        for user in users:
            for movie in movies:
                try:
                    comment, created = Comment.objects.get_or_create(
                        user=user,
                        movie=movie,
                        defaults={
                            'text': f'This is an amazing movie! {movie.title} was fantastic!'
                        }
                    )
                    if created:
                        created_comments += 1
                except Exception as e:
                    pass

        self.stdout.write(self.style.SUCCESS(f'Comments: {created_comments}'))

        self.stdout.write(self.style.SUCCESS('✅ DATABASE SEEDING COMPLETED!'))
        self.stdout.write(f'📚 Categories: {Category.objects.count()}')
        self.stdout.write(f'🎭 Genres: {Genre.objects.count()}')
        self.stdout.write(f'🎥 Movies: {Movie.objects.count()}')
        self.stdout.write(f'👥 Users: {User.objects.count()}')
        self.stdout.write(f'⭐ Ratings: {Rating.objects.count()}')
        self.stdout.write(f'💬 Comments: {Comment.objects.count()}')