#--------------------------------------------------------------------------------------------------
#
# Ingredient parser
#
# By Declan Moore, Evan Scherrer
# 
# Declan 03/07/2023: Ported the C algorithm to Python
#
#--------------------------------------------------------------------------------------------------

#of all the things Python has, it doesn't have strtol. Annoying!
def rp_parse_integer(string):
	val = 0
	for i in range(len(string)):
		chr = string[i]
		
		#if digit, continue
		int_value = ord(chr) - ord('0')
		if (int_value >= 0 and int_value <= 9):
			val *= 10
			val += int_value
		else:
			#not digit, break
			break
	
	#return a tuple: (value, remainder of string)
	return (val, string[i:])
	
"""
Parse a number in the beginning of a string. Can be a whole number, nonwhole number, or a mixed
number.

Parameters:
	string				String to parse

Returns:
	A tuple (number, string) of the parsed number and the remainder of the string unparsed.
"""
def rp_parse_quantity(string):
	part1 = 0
	part2 = 0
	(part1, string) = rp_parse_integer(string);
	
	#if next char is a point, parse this as a 2-part decimal number.
	if (len(string) > 0 and string[0] == '.'):
		string = string[1:]
		part2_start = string
		(part2, string) = rp_parse_integer(string);
		num_chars_part2 = len(part2_start) - len(string)
		
		val = part1 + (part2 * pow(0.1, num_chars_part2));
		return (val, string)
	
	#if next char is a /, parse this as a fraction.
	elif (len(string) > 0 and string[0] == '/'):
		string = string[1:]
		(part2, string) = rp_parse_integer(string);
		val = float(part1) / float(part2);
		return (val, string)
	
	#if next char is a - or space, try to parse it as a mixed number
	elif (len(string) > 0 and (string[0] == '-' or string[0] == ' ')):
		backup_str = string
		part3 = 0
		string = string[1:]
		
		(part2, string) = rp_parse_integer(string);
		if (len(string) > 0 and part2 > 0 and string[0] == '/'):
			string = string[1:]
			(part3, string) = rp_parse_integer(string)
			
			val = part1 + float(part2) / float(part3);
			return (val, string)
		else:
			#return integer (not valid mixed number)
			string = backup_str
			val = float(part1)
			return (val, string)
	
	#else, return an integer
	val = float(part1)
	return (val, string)
	
"""
Parses an ingredient string composed of a measurement and ingredient. The amount should appear
directly before the ingredient name in the string. It allows input of an integer, decimal number,
or a fixed number of the form "I N/D" or "I-N/D". Abbreviated unit names are converted into the
full singular form of the measurement name. On success, the function returns a 3-tuple of the 
amount, unit, and ingredient name. On failure, the function returns (0, None, None).

Parameters:
	string:				The string to parse

Returns:
	A tuple containing the parsed ingredient.
"""
def rp_parse_ingredient(string):
	#advance *, -, and spaces
	string = string.strip()
	while len(string) > 0 and (string[0] == '-' or string[0] == '*' or string[0] == ' '):
		string = string[1:]

	#get quantity
	(amount, string) = rp_parse_quantity(string.strip())
	
	#strip spaces
	string = string.lstrip()
	
	#tokenize
	tok = string.lower().split(" ")
	
	#if there's only one (or no) token, return error
	if (len(tok) <= 1):
		return (0, None, None)
	
	#dict of aliases and output names
	aliases = {
		#customary volumes
		"teaspoon": ["teaspoon", "teaspoons", "tsp", "tsps"],
		"tablespoon": ["tablespoon", "tablespoons", "tbsp", "tbsps"],
		"fluid ounce": ["floz", "fl", "fluid"], #if fl or fluid, consume another token
		"cup": ["cup", "cups", "c", "cs"],
		"quart": ["quart", "quarts", "qt", "qts"],
		"pint": ["pint", "pints", "pt", "pts"],
		"gallon": ["gallon", "gallons", "gal", "gals"],
		
		#customary weights
		"ounce": ["ounce", "ounces", "oz"],
		"pound": ["pound", "pounds", "lb", "lbs"],
		
		#metric volumes
		"liter": ["liter", "liters", "litre", "litres", "l"],
		"milliliter": ["milliliter", "milliliters", "millilitre", "millilitres", "ml",
			"cubic centimeter", "cubic centimeters", "cc", "ccs"],
		
		#metric weights
		"gram": ["gram", "grams", "g"],
		"kilogram": ["kilogram", "kilograms", "kg", "kgs", "kilo", "kilos"]
	}
	
	#equivalents for centimeter
	cm_aliases = ["cm", "cm.", "centimeter", "centimeters", "centimetre", "centimetres"]
	
	#equivalents for ounce
	oz_aliases = ["oz", "oz.", "ounce", "ounces"]
	
	#parse quantity. Mainly expand abbreviated unit names, and combine "fl oz" to one token
	unit_tok = tok[0]
	if unit_tok[-1] == ".":
		unit_tok = unit_tok[:-1]
	unit_name = None
	
	#scan aliases
	for name_entry in aliases.items():
		full_name = name_entry[0]
		names = name_entry[1]
		if unit_tok in names:
			unit_name = full_name
			break
	
	#if token isn't known, return an error
	if unit_name == None:
		return (0, None, None)
		
	#consume a token
	tok = tok[1:]
	if unit_tok == "fl" or unit_tok == "fluid":
		if len(tok) > 0 and (tok[0] in oz_aliases):
			tok = tok[1:]
		else:
			return (0, None, None)
	if unit_tok == "cubic":
		if len(tok) > 0 and (tok[0] in cm_aliases):
			tok = tok[1:]
		else:
			return (0, None, None)
	
	#if next token is "of", skip
	if len(tok) > 0 and tok[0] == "of":
		tok = tok[1:]
	
	return (amount, unit_name, " ".join(tok))
	
