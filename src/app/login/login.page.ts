import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from '../service/login.service';
import { ToastController } from '@ionic/angular'; // Importa ToastController para mostrar mensajes

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  user = { usuario: '', contrasena: '' };

  constructor(
    private router: Router, 
    private loginService: LoginService,
    private toastController: ToastController
  ) { }

  ngOnInit() {}

  login() {
    this.loginService.validation(this.user).subscribe({
      next: (val) => {
        console.log(val)
        if (val != null) {
          this.loginService.saveDatoLocal(val);
          this.router.navigate(['/home']);
        } else {
          this.presentToast('Usuario o contraseña incorrectos.', 'danger');
        }
      },
      error: (err) => {
        this.presentToast('Error al iniciar sesión. Intente de nuevo.', 'danger');
        console.error(err);
      }
    });
  }

  async presentToast(message: string, color: string) {
    const toast = await this.toastController.create({
      message: message,
      duration: 2000,
      color: color
    });
    toast.present();
  }
}
