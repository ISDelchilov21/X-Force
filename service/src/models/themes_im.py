from pydantic import BaseModel

class Themes(BaseModel):
   id:int
   course_id:int
   uniqInfo:str
   title:str

class ThemesCourse(BaseModel):
   course_id:int
   theme_id:int

class ThemesTest(BaseModel):
   test_id:int
   theme_test_id:int

class ThemesTest(BaseModel):
   test_id:int
   theme_homework_id:int