from django.core.management.base import BaseCommand


# python manage.py 파일에 커맨드를 생성하기 위해서는 BaseCommand를 상속하면 가능하다
class Command(BaseCommand):

    # help를 통해 --help 조건을 사용했을 때, 명령어의 설명을 추가할 수 있음
    help = "This is my first Custom Command!"

    # command에 변수를 추가하고 싶으면 add_arguments 함수를 통해 parser에 argument를 추가해줘야한다.
    def add_arguments(self, parser):
        parser.add_argument("--times", help="How many times print 'FirstCommand!'?")
        return super().add_arguments(parser)

    # 실제로 command를 실행하는 부분
    def handle(self, *args, **options):
        # options를 통해 변수를 받아올 수 있다.
        time = options.get("times")
        if time is not None:
            for k in range(int(time)):
                self.stdout.write(self.style.SUCCESS("FirstCommand!"))
        else:
            self.stdout.write(self.style.ERROR("FirstCommand!"))
