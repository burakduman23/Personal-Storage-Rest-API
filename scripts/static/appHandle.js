// register modal component
Vue.component("modal", {
    template: "#modal-template"
});

var app = new Vue({
    el: "#app",
    //------- data --------
    data: {
        serviceURL: "your url",
        authenticated: false,
        registerModal: false,
        documents: null,
        selectedDocument: null,
        loggedIn: null,
        editModal: false,
        file: null,
        input: {
            username: "",
            password: ""
        },
        registerInput: {
            firstName: "",
            lastName: "",
            email: "",
            username: "",
            password: ""
        },
        docInput: {
            doc_Name: ""
        },
        docinput: {
            docname: ""
        }
    },

    methods: {
        login() {
            if (this.input.username != "" && this.input.password != "") {
                axios
                    .post(this.serviceURL + "/login", {
                        "username": this.input.username,
                        "password": this.input.password
                    })
                    .then(response => {
                        if (response.data.status == "success") {
                            this.authenticated = true;
                            this.loggedIn = response.data.user_id;
                        }
                    })
                    .catch(e => {
                        alert("The username or password was incorrect, try again");
                        this.input.password = "";
                        console.log(e);
                    });
            } else {
                alert("A username and password must be present");
            }
        },

        logout() {
            axios
                .delete(this.serviceURL + "/login")
                .then(response => {
                    location.reload();
                })
                .catch(e => {
                    console.log(e);
                });
        },

        register() {
            axios
                .post(this.serviceURL + "/register", {
                    "firstName": this.registerInput.firstName,
                    "lastName": this.registerInput.lastName,
                    "email": this.registerInput.email,
                    "username": this.registerInput.username,
                    "password": this.registerInput.password
                })
                .then(response => {
                    if (response.data.status == "success") {
                        this.authenticated = true;
                        this.loggedIn = response.data.user_id;
                        this.registerModal = false;
                    }
                })
                .catch(e => {
                    alert("A problem occured. Make sure credentials are correct.");
                    this.registerInput.password = "";
                    console.log(e);
                });
        },
        fetchDocuments() {
            axios
                .get(this.serviceURL + "/documents")
                .then(response => {
                    this.documents = response.data.Documents;
                })
                .catch(e => {
                    alert("Unable to load the school data");
                    console.log(e);
                });
        },
        showRegister() {
            this.registerModal = true;
        },
        deleteDocument(docName) {
            if (confirm("Do you really want to delete document?")) {
                this.docInput.doc_Name = docName;
                axios
                    .delete(this.serviceURL + "/documents", { data: { 'doc_name': docName } })
                    .then(response => {
                        this.documents = this.fetchDocuments();
                    })
                    .catch(e => {
                        alert(e);
                        console.log(e);
                    });
            }

        },
        deleteUser(){
            if(confirm("Are you sure you want to delete your account?")){
                axios
                .delete(this.serviceURL+"/user")
                .then(response => {
                    this.registerModal = false;
                    this.authenticated = false;
                })
                .catch(e => {
                    alert(e);
                    console.log(e);
                });
            }
        },
        downloadDocument(doc_Name) {
        
            axios({
                method: 'post',
                url: this.serviceURL + '/user',
                responseType: 'blob',
                data: { 'doc_name': doc_Name }
            })
                .then(response => {
                    const url = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', doc_Name);
                    document.body.appendChild(link);
                    link.click();
                })
                .catch(e => {
                    alert(e);
                    console.log(e);
                });
        },

        handleUpload() {
            this.file = this.$refs.file.files[0];
        },
        submitFile() {
            let formData = new FormData();

            /*
                Add the form data we need to submit
            */
            formData.append('file', this.file, this.file.name);

            /*
              Make the request to the POST /single-file URL
            */
            axios.post('/documents',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then(function () {
                console.log('SUCCESS!!');
            })
                .catch(function () {
                    console.log('FAILURE!!');
                });
        }

    }
});