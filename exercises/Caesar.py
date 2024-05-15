
class Caesar():

	def encrypt(self, text:str, shift:int) -> str:
		"""
		Encrypts the given text using the Caesar cipher with the specified shift.
		Parameters:
			text (str): The text to encrypt.
			shift (int): The shift value for the Caesar cipher.
		Returns:
			str: The encrypted text.
		"""
		encrypted_text = ""
		for char in text:
			if char.isalpha():  # Check if the character is a letter
				shifted_char = self.upshift(char, shift)
				encrypted_text += shifted_char
			else:
				encrypted_text += char
		return encrypted_text

	def upshift(self, char:str, shift:int) -> str:
		"""
		Calculate the arithmetic shift of a character
		Parameters: 
		    char (str): ascii char a-z A-Z
			shift (int): integer in range -25,25
		Returns:
		    str: shifted character
		Raises:
		Example:
	    	let's say shift A -> Z, a shift of -1 or 25
	    	A = 65, Z = 90 so 65 + x = 90 therefore x = 25
	    	-1 mod 26 = 25, 25 mod 26 = 25
		"""
		return chr((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26 + ord('a' if char.islower() else 'A'))

	def decrypt(self, text:str, shift:int) -> str:
		"""
		Decrypts the given text using the Caesar cipher with the specified shift.
		Parameters:
			text (str): The text to decrypt.
			shift (int): The shift value for the Caesar cipher.

		Returns:
			str: The decrypted text.
		Raises:
		"""
		decrypted_text = ""
		for char in text:
			if char.isalpha():  # Check if the character is a letter
				shifted_char = chr((ord(char) - ord('a' if char.islower() else 'A') - shift) % 26 + ord('a' if char.islower() else 'A'))
				decrypted_text += shifted_char
			else:
				decrypted_text += char
		return decrypted_text	

if __name__ == '__main__':
	SHIFT = -1  # workable range -25,25
	caesar = Caesar()
	# show the shift table
	print("shift table")
	for x in range(65, 90): # chars A,Z
			y = caesar.upshift(chr(x), SHIFT)
			print (chr(x),'->',y,' ', end='')
	print(flush=True)
	message = "Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis"
	etxt = caesar.encrypt(message, SHIFT)
	print("Encrypted text")
	print(etxt)
	txt = caesar.decrypt(etxt, SHIFT)
	assert txt == message
	print("Decrypted text")
	print(txt)
