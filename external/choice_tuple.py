
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

AdminStatus = (
    ('PENDING', 'pending'),
    ('CONFIRMED', 'confirmed'),
    ('DONE', 'done'),
    ('CANCELLED', 'cancelled'),
    ('REJECTED', 'rejected'),
)

ClientOverview = (
    ('ASSIGNED', 'assigned'),
    ('ONGOING', 'ongoing'),
    ('COMPLETED', 'completed'),
    ('INCOMPLETE', 'incomplete'),
)


PackageType = (
        ('SINGLE', 'single'),
        ('FIVE', 'five'),
)

ReviewStatus = (
    ('PENDING', 'pending'),
    ('ACCEPTED', 'accepted'),
    ('REJECTED', 'rejected'),
)