def add_staff(request):
    if request.method == 'POST':
        # ... rest of the validation code ...

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        Staff.objects.create(admin=user, address=address)  # Use admin instead of user

        messages.success(request, "Staff added successfully.")
        return redirect('manage_staff')

    return render(request, 'admin_app/add_staff.html')