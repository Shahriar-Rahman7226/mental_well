
UserRole = (
    ('ADMIN', 'admin'),
    ('COUNSELOR', 'counselor'),
    ('CLIENT', 'client'),
)

PaymentMethodType = (
    ('CASH', 'cash'),
    ('BKASH', 'bkash'),
    # ('BANK', 'bank'),
    # ('NAGAD', 'nagad'),
    # ('ROCKET', 'rocket'),
    # ('VISA', 'visa'),
    # ('MASTER_CARD', 'master_card'),
)

ProfileStatus = (
    ('PENDING', 'pending'),
    ('APPROVED', 'approved'),
    ('REJECTED', 'rejected'),
)

Gender = (
    ('MALE', 'male'),
    ('FEMALE', 'female'),
    ('OTHER', 'other')
)

Days = (
    ('SUNDAY', 'sunday'),
    ('MONDAY', 'monday'),
    ('TUESDAY', 'tuesday'),
    ('WEDNESDAY', 'wednesday'),
    ('THURSDAY', 'thursday'),
    ('FRIDAY', 'friday'),
    ('SATURDAY', 'saturday'),
)

AppointmentStatus = (
    ('PENDING', 'pending'),
    ('CONFIRMED', 'confirmed'),
    ('DONE', 'done'),
    ('CANCELLED', 'cancelled'),
)