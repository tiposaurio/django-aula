# This Python file uses the following encoding: utf-8
from django.db.models import get_model

#-------------Impartir-------------------------------------------------------------      

def impartir_clean( instance ):
    pass

def impartir_pre_delete( sender, instance, **kwargs):
    pass
    
def impartir_pre_save(sender, instance,  **kwargs):
    instance.clean()

def impartir_post_save(sender, instance, created, **kwargs):
    #bussiness rule:
    #si un professor passa llista, també passa llista de 
    #totes les imparticions que no tinguin alumnes.
    if instance.professor_passa_llista is not None:
        Impartir = get_model('presencia','Impartir')
        altresHores = Impartir.objects.filter( horari__hora = instance.horari.hora, 
                                               dia_impartir = instance.dia_impartir,
                                               controlassistencia__isnull = True,
                                               horari__professor = instance.horari.professor,
                                               horari__grup__isnull = False  )
        
        altresHores.update( professor_passa_llista = instance.professor_passa_llista,
                           dia_passa_llista = instance.dia_passa_llista )
    
    pass

def impartir_despres_de_passar_llista(instance):
    #Si passa llista un professor que no és el de l'Horari cal avisar.
    if instance.professor_passa_llista <> instance.horari.professor:
        remitent = instance.professor_passa_llista
        text_missatge = u"""Has passat llista a un grup que no és el teu: ({0}). 
                         El professor del grup {1} rebrà un missatge com aquest.
                         """.format( unicode(instance),  unicode(instance.horari.professor) )
        Missatge = get_model( 'missatgeria','Missatge')
        msg = Missatge( remitent = remitent.getUser(), text_missatge = text_missatge )           
        msg.envia_a_usuari( usuari = instance.professor_passa_llista.getUser(), importancia = 'VI')

        text_missatge = u"""Ha passat llista d'una classe on consta que la fas tú: ({0}). 
                         """.format( unicode(instance),  unicode(instance.horari.professor) )
        msg = Missatge( remitent = remitent.getUser(), text_missatge = text_missatge )           
        msg.envia_a_usuari( usuari = instance.horari.professor.getUser(), importancia = 'VI')
    

