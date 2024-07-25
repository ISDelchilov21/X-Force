from pydantic import BaseModel


class ThemesIM(BaseModel):
    id: int
    class_id: int
    owner_id: int
    unique_info: str
    title: str


class ThemeGetIM(BaseModel):
    title: str


class ThemesClasssIM(BaseModel):
    course_id: int
    theme_id: int


class ThemesTestIM(BaseModel):
    test_id: int
    theme_test_id: int


class ThemesTestIM(BaseModel):
    test_id: int
    theme_homework_id: int
