from django import template

register = template.Library()

#arg contains whole string that is passed to function in jinja
#value is a value attribute of django form object 
#value when printed contains string with html code of tag that in jinja called from
def htmlAttrib(value, arg):
	attrs = value.field.widget.attrs #Getting already existing attributes of form as dictionary
	data = arg.replace(' ','') #Replacing any space cuz html allows it
	kvs = data.split(',') #Spliting every attribute with its value assigned
	print("DEBUG:")
	print(attrs)

	for string in kvs:
		kv = string.split(":") #Spliting attribute and its value
		attrs[kv[0]] = kv[1] #Adding or overwriting if exist entry in dictionary that holds all attributes of html tag

	rendered = str(value) #casting value object to string what causes that rendered will now have html code of tag
	return rendered

register.filter('htmlAttrib', htmlAttrib)