#--------------------------------------------------------------------------------------------------
#
# Ingredient parser utils
#
# By Declan Moore, Evan Scherrer
# 
# Declan 03/07/2023: Ported the C algorithm to Python
# Evan 03/07/2023: copied it all to a new file B)
#
#--------------------------------------------------------------------------------------------------


def rp_parse_integer(string):
	val = 0
	i = 0
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
		
		#HACK: Python does for loops weirdly, so this is necessary
		if i == len(string) - 1:
			i += 1
	
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
def rp_parse_ingredient_unit_prefix(string):
	#advance *, -, and spaces
	string = string.strip()
	while len(string) > 0 and (string[0] == '-' or string[0] == '*' or string[0] == ' '):
		string = string[1:]

	#get quantity
	(amount, string) = rp_parse_quantity(string.strip())
	
	#strip spaces
	string = string.lstrip()
	
	#tokenize
	tok = string.split(" ")
	
	#if there's no token, return error
	if (len(tok) == 0):
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
	if len(unit_tok) > 0 and unit_tok[-1] == ".":
		unit_tok = unit_tok[:-1]
	unit_name = None
	
	#scan aliases
	for name_entry in aliases.items():
		full_name = name_entry[0]
		names = name_entry[1]
		if unit_tok.lower() in names:
			unit_name = full_name
			break
	
	#check for t or T (teaspoon 
	if unit_tok == "t":
		unit_name = "teaspoon"
	elif unit_tok == "T":
		unit_name = "tablespoon"
	
	#if token isn't known, return it as a count if it's an integer. Otherwise, error.
	if unit_name == None and amount == int(amount) and amount > 0:
		ingredient = " ".join(tok).strip()
		if len(ingredient) > 0:
			return (amount, "count", " ".join(tok))
		else:
			return (0, None, None)
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
	
	return (amount, unit_name, " ".join(tok).strip().lower())

"""
Check the return value of ingredient parsing to determine if the parse was
successful or not.

Parameters:
	ingredient_tuple:	The return from parsing

Returns:
	True if the parsing was successful, false otherwise.
"""
def rp_parse_success(ingredient_tuple):
	if ingredient_tuple[0] == 0 or ingredient_tuple[1] == None or ingredient_tuple[2] == None:
		return False
	return True

"""
Get a complete list of indices of occurrences of a set of characters in a
string.

Parameters:
	string:				The string to search
	chars:				The set of characters to search for

Returns:
	A list of indices of occurrences of characters in the string.
"""
def rp_strchr_multi(string, chars):
	#build a list of indices to this char
	indices = []
	
	index = 0
	for c in string:
		if c in chars:
			indices.append(index)
		index += 1
		
	return indices

"""
Performs substitutions specified in a map on a string. Keys from the map are
replaced by their corresponding values.

Parameters:
	string:				The string to perform substitutions on
	map:				The map containing the substitutions

Returns:
	The input string after processing all of the substitutions.
"""
def rp_perform_substitutions(string, map):
	#perform all substitutions
	out = string
	for entry in map.items():
		key = entry[0]
		val = entry[1]
		if key in out:
			out = out.replace(key, val)
	
	return out

"""
Parses an ingredient string composed of a measurement and ingredient. If the
ingredient parsing succeeds, it returns a tuple containing (amount, unit, name).
If it fails, it returns a tuple (0, None, None).

Parameters:
	string:				The string to parse

Returns:
	A tuple containing the parsed ingredient.
"""
def rp_parse_ingredient(string):
	#process Unicode substitutions
	string = rp_perform_substitutions(string, {
		"¼":	" 1/4",		#00BC
		"½":	" 1/2",		#00BD
		"¾":	" 3/4",		#00BE
		"⅐":	" 1/7",		#2150
		"⅑":	" 1/9",		#2151
		"⅒":	" 1/10",	#2152
		"⅓":	" 1/3",		#2153
		"⅔":	" 2/3",		#2154
		"⅕":	" 1/5",		#2155
		"⅖":	" 2/5",		#2156
		"⅗":	" 3/5",		#2157
		"⅘":	" 4/5",		#2158
		"⅙":	" 1/6",		#2159
		"⅚":	" 5/6",		#215A
		"⅛":	" 1/8",		#215B
		"⅜":	" 3/8",		#215C
		"⅝":	" 5/8",		#215D
		"⅞":	" 7/8",		#215E
		
		#to make tokenization a little easier
		")":	" )"
	})
	string = string.strip()
	
	#try parse as normal
	try_parsed = rp_parse_ingredient_unit_prefix(string)
	if (try_parsed[0] > 0 and try_parsed[1] != None and try_parsed[2] != None):
		return try_parsed
	
	#there was one or more problems parsing.
	#try the string token by token.
	tok_indices = rp_strchr_multi(string, " -(),") #characters we expect could separate parts
	
	for tok_index in tok_indices:
		separator = string[tok_index]
		post = string[tok_index + 1:]
		try_parsed = rp_parse_ingredient_unit_prefix(post)
		
		if rp_parse_success(try_parsed):
			#fix up output string to exclude unit. 
			#TODO: more advanced processing if necessary?
			new_ingredient_name = string[0:tok_index].strip()
			return (try_parsed[0], try_parsed[1], new_ingredient_name)
	
	#in failure
	return (0, None, None)
