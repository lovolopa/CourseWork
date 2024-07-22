from src.reports import main_reports
from src.services import main_services
from src.views import main_views


def main() -> None:
    """Отвечает за основную логику проекта с пользователем"""
    main_views()
    main_services()
    main_reports()


if __name__ == '__main__':
    main()
