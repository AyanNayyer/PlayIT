export default {
    template: `
    <div>
    <div v-if="role.includes('artist')" class="text-center mt-4">
        <h2><u>Artist's Dashboard</u></h2>
    </div>

    <div v-if="role.includes('artist')" class="container mt-4">
        <div class="row">
            <div v-for="(stat, index) in artistStats" :key="index" class="col-lg-4 mb-4">
                <div class="card" style="background-color: lightyellow;">
                    <div class="card-body">
                        <h3 class="card-text">{{ stat.title }}: {{ stat.value }}</h3>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div v-if="role.includes('artist')" class="text-center mt-4">
        <h3>Your Uploads:</h3>
    </div>

    <div v-if="my_songs.length !== 0" class="table-responsive mt-3">
        <table class="table table-bordered table-hover">
            <thead>
                <tr>
                    <th>Song</th>
                    <th>Album</th>
                    <th>Likes</th>
                    <th>Views</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="song in my_songs" :key="song.id">
                    <td>{{ song.name }}</td>
                    <td>{{ song.album_name }}</td>
                    <td>{{ song.likes }}</td>
                    <td>{{ song.play_count }}</td>
                    <td>
                        <button type="button" class="btn btn-danger" @click="delete_upload(song.id)">Delete</button>
                        <button type="button" class="btn btn-primary" @click="edit_upload(song.id)">Edit</button>
                        <div v-if="edit_upload_clicked[song.id]" class="mt-3">
                            <form @submit.prevent="save_changes(song.id)">
                                <label for="title" class="form-label">Title</label>
                                <input v-model="song_name" type="text" name="title" id="title" class="form-control" required>
                                <!-- (Similar adjustments for other form fields) -->
                                <button type="submit" class="btn btn-success mt-2">Save Changes</button>
                                <button type="button" class="btn btn-secondary mt-2" @click="cancel(song.id)">Cancel</button>
                            </form>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="text-center mt-3" v-if="role.includes('artist')">
        <button type="button" class="btn btn-primary" @click="upload">Add to uploads</button>
    </div>

    <div v-else class="text-center mt-4">
        <h3>Would you like to Register as an Artist</h3>
        <div class="text-center mt-3">
            <button type="button" class="btn btn-primary" @click="register">Register</button>
        </div>
    </div>
    <div v-if="role.includes('artist')" class="text-center mt-4">
    <h3>Your Albums:</h3>
    </div>

    <div v-if="my_albums.length !== 0" class="table-responsive mt-3">
    <table class="table table-bordered table-hover">
        <thead>
            <tr>
                <th>Album</th>
                <th>Year</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="album in my_albums" :key="album.id">
                <td>{{ album.name }}</td>
                <td>{{ album.year }}</td>
                <td>
                    <button type="button" class="btn btn-danger" @click="delete_album(album.id)">Delete</button>
                    <button type="button" class="btn btn-primary" @click="edit_album(album.id)">Edit</button>
                    <!-- Add a form for editing the album name -->
                    <div v-if="edit_album_clicked[album.id]" class="mt-3">
                        <form @submit.prevent="save_album_changes(album.id)">
                            <label for="albumName" class="form-label">Album Name</label>
                            <input v-model="album_name" type="text" name="albumName" id="albumName" class="form-control" required>
                            <label for="albumYear" class="form-label">Album Year</label>
                            <input v-model="album_year" type="number" name="albumYear" id="albumYear" class="form-control" required>
                            <button type="submit" class="btn btn-success mt-2">Save Changes</button>
                            <button type="button" class="btn btn-secondary mt-2" @click="cancel_album_edit(album.id)">Cancel</button>
                        </form>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
    </div>
</div>

    `,

    data(){
        return{
            role: localStorage.getItem('role'),
            my_songs: [],
            my_albums: [],
            edit_album_clicked: {},

            artistStats: [
                { title: 'Total Uploads', value: 0 },
                { title: 'Total Likes', value: 0 },
                { title: 'Total Albums', value: 0 }
            ],

            song_name: '',
            album_name: '',
            album_year:'',
            genre: '',
            year: 0,
            duration: 0,
            lyrics: '',
            song_file: null,
            edit_upload_clicked: {},

            token: localStorage.getItem('auth_token'),
            
        }
    },
    async mounted(){
        try{
            await this.your_uploads();
            await this.your_albums();
            await this.artist_statistics();}
        catch(err){
            console.log("not an artist");
        }    
    },
    
    methods: {
        async register(){
            const confirm_register = window.confirm("Are you sure you want to become an artist?")

            if (confirm_register == true){
                const response = await fetch('/artist_register', {
                    method: 'POST',
                    headers: {
                        'Authentication-Token': this.token
                    },
                })
                if (response.status == 200) {
                    const response_data = await response.json();
                    localStorage.setItem('role', response_data.role);
                    alert(response_data.message);
                    window.location.reload();
                }
                else {
                    const error = await response.json();
                    alert(error.message);
                }
            }
            else{
                return
            }
        },

        artist_statistics() {
            this.$set(this.artistStats, 0, { title: 'Total Uploads', value: this.my_songs.length });
            this.$set(this.artistStats, 1, { title: 'Total Likes', value: this.my_songs.reduce((a, b) => a + b.likes, 0) });
            
            const albums_set = new Set();
            for (let i = 0; i < this.my_songs.length; i++) {
                albums_set.add(this.my_songs[i].album_id);
            }
            this.$set(this.artistStats, 2, { title: 'Total Albums', value: albums_set.size });
        },

        upload(){
            return this.$router.push('/api/manage_albums')
        },

        async your_uploads() {
            try {
                const response = await fetch('/your_uploads', {
                    method: 'GET',
                    headers: {
                        'Authentication-Token': this.token
                    },
                });
        
                if (response.status == 200) {
                    const response_data = await response.json();
                    this.my_songs = response_data.songs;
        
                    // Now that we have fetched the uploads, update the statistics
                    this.artist_statistics();
                } else {
                    const error = await response.json();
                    alert(error.message);
                }
            } catch (error) {
                console.error('Error fetching uploads:', error);
            }
        },

        async delete_upload(song_id) {
            const confirm_delete = window.confirm("Are you sure you want to delete this song?");
        
            if (confirm_delete) {
                const response = await fetch(`/delete_upload/${song_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                });
        
                if (response.status === 200) {
                    const response_data = await response.json();
                    alert(response_data.message);
                    // Explicitly call the methods to update artist's uploads and statistics
                    await this.your_uploads();
                    this.artist_statistics();
                } else {
                    const error = await response.json();
                    alert(error.message);
                }
            }

        },
        
        edit_upload(song_id){
            this.$set(this.edit_upload_clicked, song_id, true);
            this.song_name = this.my_songs.find(song => song.id == song_id).name;
            this.album_name = this.my_songs.find(song => song.id == song_id).album_name;
            this.genre = this.my_songs.find(song => song.id == song_id).genre;
            this.year = this.my_songs.find(song => song.id == song_id).year;
            this.duration = this.my_songs.find(song => song.id == song_id).duration;
            this.lyrics = this.my_songs.find(song => song.id == song_id).lyrics;
            
        },
        cancel(song_id){
            this.$set(this.edit_upload_clicked, song_id, false);
        },

        async save_changes(song_id){
            const formData = new FormData();
            formData.append('song_name', this.song_name);
            formData.append('album_name', this.album_name);
            formData.append('genre', this.genre);
            formData.append('year', this.year);
            formData.append('duration', this.duration);
            formData.append('lyrics', this.lyrics);
            
            const response = await fetch(`/save_changes/${song_id}`, {
                method: 'POST',
                headers: {
                    'Authentication-Token': this.token
                },
                body: formData
            })
            if (response.status == 200) {
                const response_data = await response.json();
                alert(response_data.message);
                window.location.reload();
            }
            else {
                const error = await response.json();
                alert(error.message);
            }
        },

        async your_albums() {
            try {
                const response = await fetch('/your_albums', {
                    method: 'GET',
                    headers: {
                        'Authentication-Token': this.token
                    },
                });
    
                if (response.status == 200) {
                    const response_data = await response.json();
                    this.my_albums = response_data.albums;
                } else {
                    const error = await response.json();
                    alert(error.message);
                }
            } catch (error) {
                console.error('Error fetching albums:', error);
            }
        },
    
        edit_album(album_id) {
            this.$set(this.edit_album_clicked, album_id, true);
            this.album_name = this.my_albums.find(album => album.id == album_id).name;
            this.album_year = this.my_albums.find(album => album.id == album_id).year;
        },
        cancel_album_edit(album_id) {
            this.$set(this.edit_album_clicked, album_id, false);
        },
        
        async save_album_changes(album_id) {
            const formData = new FormData();
            formData.append('name', this.album_name);
            formData.append('year', this.album_year);
        
            const response = await fetch(`/api/edit_delete_album/${album_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token
                },
                body: JSON.stringify(Object.fromEntries(formData.entries()))
            });
        
            if (response.status == 200) {
                const response_data = await response.json();
                alert(response_data.message);
                window.location.reload();
            } else {
                const error = await response.json();
                alert(error.message);
            }
        },
    
        async delete_album(album_id) {
            const confirm_delete = window.confirm("Are you sure you want to delete this album?");
    
            if (confirm_delete) {
                const response = await fetch(`api/edit_delete_album/${album_id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                });
    
                if (response.status === 200) {
                    const response_data = await response.json();
                    alert(response_data.message);
                    await this.your_albums();
                } else {
                    const error = await response.json();
                    alert(error.message);
                }
            }
        },
    } 
}

