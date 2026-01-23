import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private url = `${environment.apiUrl}`;

  // Constantes para el almacenamiento local
  private static readonly TOKEN_KEY = 'token';
  private static readonly USUARIO_KEY = 'usuario';
  private static readonly PASSWORD_KEY = 'contrasena';

  constructor(private http: HttpClient) { }

  // Método para validar el usuario
  validation(us: any): Observable<any> {
    const body = new HttpParams().set('usuario', us.usuario).set('contrasena', us.contrasena);
    return this.http.post(this.url + '/api/login', body.toString(), {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    });
  }
  getSolicitudes(seq:number, token: string):Observable<any[]>{
    const hheaders = new HttpHeaders({
      'Content-type': 'application/json',
      'Authorization': token
    })
    console.log(hheaders)
    return this.http.get<any[]>(this.url+'/api/solicitudservicio/datos/'+seq, {headers: hheaders})
  }

  // Métodos para manejar el token, usuario y contraseña en localStorage
  public setToken(token: string): void {
    window.localStorage.setItem(LoginService.TOKEN_KEY, token);
  }

  public getToken(): string {
    return window.localStorage.getItem(LoginService.TOKEN_KEY) || '';
  }

  public setUsuario(usuario: string): void {
    window.localStorage.setItem(LoginService.USUARIO_KEY, usuario);
  }

  public getUsuario(): string {
    return window.localStorage.getItem(LoginService.USUARIO_KEY) || '';
  }

  public setPassword(password: string): void {
    window.localStorage.setItem(LoginService.PASSWORD_KEY, password);
  }

  public getPassword(): string {
    return window.localStorage.getItem(LoginService.PASSWORD_KEY) || '';
  }

  public cerrarSesion(): void {
    window.localStorage.clear();
  }

  // Método para guardar los datos del usuario después de un inicio de sesión exitoso
  public saveDatoLocal(data: any): void {
    localStorage.setItem('data', JSON.stringify(data))
    console.log(data  )
    this.setToken(data.token);
    this.setUsuario(data.usuario);
    this.setPassword(data.contrasena);
  }
}
