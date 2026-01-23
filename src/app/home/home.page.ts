import { Component } from '@angular/core';
import { LoginService } from '../service/login.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  constructor(private login:LoginService) {}
  solicitudes:any[]=[]
  user:any

  ngOnInit(){
    this.user =JSON.parse(localStorage.getItem('data')!)
    console.log('hola')
    this.login.getSolicitudes(this.user.persona.seq_persona, this.user.token).subscribe(list =>{
      console.log(list)
      this.solicitudes=list
    })
  }

}
