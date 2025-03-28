from django.utils.timezone import now, timedelta
from .models import User, Doctor, Appointment

def create_appointment(user_name, user_email, doctor_name):
    try:
        # Create or get existing user
        user, _ = User.objects.get_or_create(name=user_name, email=user_email)

        # Find an available doctor
        doctor = Doctor.objects.filter(name__iexact=doctor_name, available=True).first()
        if not doctor:
            return f"Sorry, Dr. {doctor_name} is not available at the moment."

        # Check if the doctor already has an appointment scheduled in the next hour
        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__gte=now(),
            appointment_date__lte=now() + timedelta(hours=1)
        ).exists()

        if existing_appointment:
            return f"Sorry, Dr. {doctor.name} already has an appointment scheduled."

        # Create appointment
        appointment = Appointment.objects.create(
            user=user,
            doctor=doctor,
            appointment_date=now() + timedelta(minutes=30)  # Book 30 mins from now
        )

        # Mark doctor as unavailable (optional)
        doctor.available = False
        doctor.save()

        return f"Appointment created with Dr. {doctor.name} at {appointment.appointment_date.strftime('%Y-%m-%d %H:%M:%S')}."

    except Exception as e:
        return f"Failed to create appointment: {str(e)}"
