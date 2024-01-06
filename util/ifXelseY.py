# Returns the first value in the parameters which has been defined.
def ifXelseY(x, y):
    if x in locals():
        return x
    return y
