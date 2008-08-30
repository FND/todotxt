def containsAny(seq, terms):
	"""
	check whether a sequence contains any of the given terms

	@param seq (str, list, tuple): sequence to investigate
	@param terms (list, tuple): terms to match
	@return (bool): match
	"""
	for t in terms:
		if t in seq:
			return True
	return False

def containsAll(seq, terms):
	"""
	check whether a sequence contains all of the given terms

	@param seq (str, list, tuple): sequence to investigate
	@param terms (list, tuple): terms to match
	@return (bool): match
	"""
	for t in terms:
		if t not in seq:
			return False
	return True

