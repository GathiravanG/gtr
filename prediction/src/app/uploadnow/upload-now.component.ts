import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup } from '@angular/forms';


@Component({
  selector: 'app-upload-now',
  templateUrl: './upload-now.component.html',
  styleUrls: ['./upload-now.component.css']
})
export class UploadNowComponent implements OnInit {

   file: File = null as any; // Variable to store file
   form1: FormGroup = null as any;
   postdata: any
   value: any
   val: any
   
   // Inject service 
   constructor(private http:HttpClient , private fb:FormBuilder) {}
 
   ngOnInit(): void {
    this.form1 = this.fb.group({
      predictingcolumn:['']
    })

   }
 
   // On file Select
   onChange(event:any) {
       console.log(event)
       this.file = <File> event.target.files[0];
   }


   onFileUpload() {

    const formData = new FormData();
       formData.append('file', this.file, this.file.name);
       this.http.post("http://127.0.0.1:5000/uploadnow", formData).subscribe((event)=>{
        console.log(event);
       });
   }

   
   // OnClick of button Upload
   onUpload() {
       
       this. postdata={
        period:this.value,
        target:this.val
       };

       this.http.post("http://127.0.0.1:5000/column", JSON.stringify(this.form1.value)).subscribe((event)=>{
        console.log(this.form1.value);
       });
       
       this.http.post("http://127.0.0.1:5000/period", (this.postdata)).subscribe((res)=>{
        console.log(res);
        alert(res);
       });
       console.log(this.value)
       console.log(this.val)
       console.log("Started predicting")
       
    }

}
