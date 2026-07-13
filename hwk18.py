#    შექმენით მეტაკლასი, რომელიც სხვა კლასზე გამოყენების შემთხვევაში შეამოწმებს ამ კლასის მეთოდის სახელებს,
#    შემდეგი სახით: თუ მეთოდი იწყება _ ეს მეთოდი ვალიდური იქნება, თუ არ იწყება _, მაშინ აღზევდეს 
#    ValueError. მაგ: _test() - ეს მეთოდი იქნება ვალიდური, test() - ეს მეთოდი არ იქნება ვალიდური
#    და გამოიწვევს ValueError-ს. გაითვალისწინეთ რომ მეტაკლასმა უნდა შეამოწმოს მხოლოდ მეთოდები და არა ატრიბუტები!


class MethodNameValidator(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                raise ValueError(f"Method '{attr_name}' is not valid. Method names must start with an underscore.")
        return super().__new__(cls, name, bases, attrs)
        