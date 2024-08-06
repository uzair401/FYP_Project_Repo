def validate_marks(obtained_internal, obtained_mid, obtained_final, course_internal, course_mid, course_final, course_total):
    if obtained_internal < 0 or obtained_mid < 0 or obtained_final < 0:
        return False
    if (obtained_internal <= course_internal and
        obtained_mid <= course_mid and
        obtained_final <= course_final and
        (obtained_internal + obtained_mid + obtained_final) <= course_total):
        return True
    else:
        return False
