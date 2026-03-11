const app = new Vue({
    el: '#app',
    data: {
        alunos: [],
        novoAluno: {
            nome: '',
            telefone: '',
            idade: '',
            contato: '',
            modalidade: '',
            plano: '',
            mensalidade: '',
            observacao: ''
        },
        backendUrl: 'http://192.168.1.22:8000/alunos'
    },
    methods: {
        listarAlunos() {
            fetch(this.backendUrl)
                .then(res => res.json())
                .then(data => this.alunos = data);
        },
        adicionarAluno() {
            fetch(this.backendUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.novoAluno)
            })
            .then(() => {
                this.novoAluno = { nome: '', telefone: '', idade: '', contato: '', modalidade: '', plano: '', mensalidade: '', observacao: '' };
                this.listarAlunos();
            });
        },
        excluirAluno(id) {
            fetch(`${this.backendUrl}/${id}`, { method: 'DELETE' })
                .then(() => this.listarAlunos());
        }
    },
    mounted() {
        this.listarAlunos();
    }
});
