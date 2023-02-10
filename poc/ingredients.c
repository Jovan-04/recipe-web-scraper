#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>

typedef enum Unit_ {
	U_Unknown,
	U_Teaspoon,
	U_Tablespoon,
	U_CubicInch, //TODO
	U_Cup,
	U_Pint, //TODO
	U_Quart, //TODO
	U_Gallon, //TODO
	U_Ounce, //TODO
	U_FluidOunce, //TODO
	U_Pinch, //TODO
	U_Dash
} Unit;

/*
Key:
n - number (integer, decimal, fraction)
u - unit
i - ingredient
Text format:
n u i
nu i
*/

char *parseInteger(char *str, char *end, int *out) {
	int n = 0;
	while (str < end) {
		char c = *str;
		if (c < '0' || c > '9') break;
		
		n *= 10;
		n += c - '0';
		str++;
	}
	
	*out = n;
	return str;
}

/*
Parse a string as a quantity. May be an integer, decimal, or fraction.
*/
char *parseQuantity(char *str, char *end, float *out) {
	int part1 = 0, part2 = 0;
	str = parseInteger(str, end, &part1);
	
	//if next char is a point, parse this as a 2-part decimal number.
	if (str < end && *str == '.') {
		str++;
		char *part2Start = str;
		str = parseInteger(str, end, &part2);
		int nCharsPart2 = str - part2Start;
		
		*out = part1 + (part2 * pow(0.1, nCharsPart2));
	}
	
	//if next char is a /, parse this as a fraction.
	else if (str < end && *str == '/') {
		str++;
		str = parseInteger(str, end, &part2);
		*out = ((float) part1) / ((float) part2);
	}
	
	//if next char is a - or space, try to parse it as a mixed number
	else if (str < end && (*str == '-' || *str == ' ')) {
		char *backupStr = str;
		char sep = *str;
		int part3 = 0;
		str++;
		
		str = parseInteger(str, end, &part2);
		if (str < end && part2 > 0 && *str == '/') {
			str++;
			str = parseInteger(str, end, &part3);
			
			*out = part1 + (((float) part2) / ((float) part3));
		} else {
			//return integer (not valid mixed number)
			str = backupStr;
			*out = (float) part1;
		}
	}
	
	//else, return an integer
	else {
		*out = (float) part1;
	}
	
	return str;
}

int stringEqual(const char *s1, int nChars, const char *s2) {
	for (int i = 0; i < nChars; i++) {
		char c1 = s1[i];
		char c2 = s2[i];
		if (c2 == '\0') return 0;
		if (c1 != c2) return 0;
	}
	return 1;
}

char *parseUnit(char *str, char *end, Unit *outUnit) {
	//read chars until we hit a non-alphabetic character
	char *base = str;
	int nCharsUnit = 0;
	while (str < end && ((*str >= 'a' && *str <= 'z') || (*str >= 'A' && *str <= 'Z'))) str++;
	
	nCharsUnit = str - base;
	if (stringEqual(base, nCharsUnit, "tsp") || stringEqual(base, nCharsUnit, "teaspoon")
		|| stringEqual(base, nCharsUnit, "teaspoons")) {
		
		*outUnit = U_Teaspoon;
	} else if (stringEqual(base, nCharsUnit, "tbsp") || stringEqual(base, nCharsUnit, "tablespoon")
		|| stringEqual(base, nCharsUnit, "tablespoons")) {
		
		*outUnit = U_Tablespoon;
	} else if (stringEqual(base, nCharsUnit, "c") || stringEqual(base, nCharsUnit, "cup")
		|| stringEqual(base, nCharsUnit, "cups")) {
		
		*outUnit = U_Cup;
	} else {
		*outUnit = U_Unknown;
	}
	
	//if there's a dot after the unit, advance
	if (str < end && *str == '.') str++;
	
	return str;
}

char *parseRealQuantity(char *str, char *end, float *outAmount, Unit *outUnit) {
	char *start = str;
	float amount;
	Unit unit;
	
	//try parse quantity
	str = parseQuantity(str, end, &amount);
	
	//check that a quantity was parsed. 
	if (str > start) {
		//great. If next char is a space, advance.
		char *unitStart = str;
		while (str < end && *str == ' ') str++;
		
		//parse unit. agh
		str = parseUnit(str, end, &unit);
		if (str > unitStart) {
			if (str < end && *str == '.') str++;
			while (str < end && *str == ' ') str++;
			
			//if there's at least 3 characters to go, try skipping "of " if it exists.
			if (str + 3 <= end) {
				char c0 = toupper(str[0]);
				char c1 = toupper(str[1]);
				char c2 = toupper(str[2]);
				
				if (c0 == 'O' && c1 == 'F' && c2 == ' ') str += 3;
				while (str < end && *str == ' ') str++;
			}
			
			*outUnit = unit;
			*outAmount = amount;
			return str;
		}
	}
	
	//failure, backtrack
	str = start;
	
	*outUnit = U_Unknown;
	*outAmount = 0.0f;
	return str;
}

char *parseLine(char *str, char *end, float *outAmount, Unit *outUnit, char *outIngredient, int nMaxChars) {
	char *start = str;
	float amount = 0.0f;
	Unit unit = U_Unknown;
	
	//if line starts with *, -, or space, advance.
	while (str < end && (*str == '*' || *str == '-' || *str == ' ')) str++;
	
	str = parseRealQuantity(str, end, &amount, &unit);
	
	//check that a quantity was parsed. 
	if (str > start) {
		//leftover is ingredient
		while (nMaxChars > 0 && str < end && (*str != '\n' && *str != '\r')) {
			char c = *(str++);
			c = toupper(c);
			*(outIngredient++) = c;
			nMaxChars--;
		}
	} else {
		//
		//uh
	}
	
	*outUnit = unit;
	*outAmount = amount;
	return str;
}

int main(void) {
	char *str = "";
	float quant = 0;
	Unit unit;
	char ingredientBuffer[32] = {0};
	parseLine(str, str + strlen(str), &quant, &unit, ingredientBuffer, sizeof(ingredientBuffer) - 1);
	
	printf("%f %d of %s\n", quant, unit, ingredientBuffer);
	
	return 0;
}