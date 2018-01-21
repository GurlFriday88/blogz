
def validate_len(form_input):
    #check for presence of input
    form_value = form_input
    error = ''
    if not form_input:
        error = "Why you no enter {name} !?"

    elif len(form_value) < 3 or len(form_value) > 20:  # check for length
        error = "I need something between (3-20) characters"

    elif " " in form_value:  # check for spaces
        error = "Me no likey {name} with spaces"
    return error

def validate_pass_email():
    user_name_error = ""
    password_error = ""
    verify_pass_error = ""
    compare_pass_error = ""
    email_error = ""
    # #checks for validation of username, password, and verify password
    user_name_error = validate_len(user_name).format(name="Username")
    password_error = validate_len(password).format(name="Password")
    verify_pass_error = validate_len(verify_password).format(name="Verify Password")

    # #compare password to verify password
    if verify_password not in password:
        compare_pass_error = "NONE SHALL PASS!...Without matching passwords"
    #check for @ and . symbols
    if not re.search(r"([a-z]+[@]+[a-z]+[.]+[a-z])", email):
        email_error = "Can I get an actual email address?"
    else:
        email_error = validate_len(email).format(name="Email")  # complete email validation
    #checks for empty error messages. If the validation passed the welcome page will be generated
    if not (user_name_error or
            password_error or
            verify_pass_error or
            compare_pass_error or
            email_error
            ):
        return redirect('welcome?user_name={0}'.format(user_name))
    return render_template('signup-page.html',
                            username_error=user_name_error,
                            password_error=password_error,
                            verify_pass_error=verify_pass_error,
                            compare_pass_error=compare_pass_error,
                            email_error=email_error,
                            user_name=user_name,
                            )
return render_template('signup-page.html', title="User Sign Up Page")


@app.route('/welcome')
def welcome_user():
    user_name = request.args.get('user_name')
    return render_template('welcome.html', user_name=user_name)


app.run()
