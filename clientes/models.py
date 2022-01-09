from django.db import models
from django.core.mail import send_mail, mail_admins, send_mass_mail
from django.template.loader import render_to_string


class Documento(models.Model):
    num_doc = models.CharField(max_length=50)

    def __str__(self):
        return self.num_doc


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    bio = models.TextField()
    photo = models.ImageField(upload_to='clients_photos', null=True, blank=True)
    doc = models.OneToOneField(Documento, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('deletar_clientes', 'Deletar clientes'),
        )


    @property
    def nome_completo(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs)
        print("email_1")
        data = {'cliente': self.first_name}
        print("email_2")
        plain_text = render_to_string('clientes/emails/novo_cliente.txt', data)
        print("email_3")
        html_email = render_to_string('clientes/emails/novo_cliente.html', data)
        print("email_4")
        
        print("email_5")
        mail_admins(
            'Olá admin tem um novo cliente cadastrado',
            plain_text,
            html_message=html_email,
            fail_silently=False,
        )
        print("email_6")
        message1 = (
            'Subject here', 'Here is the message', 'felipe.brx.dev@gmail.com',
            ['centro.setelinhas@gmail.com', ])
        print("email_7")
        message2 = ('Another Subject', 'Here is another message', 'felipe.brx.dev@gmail.com',
                    ['felipe.brx.dev@gmail.com', ])
        print("email_8")
        send_mass_mail([message1, message2], fail_silently=False)
        print("email_9")

    def __str__(self):
        return self.first_name + ' ' + self.last_name






