export default {
    template: 
    `<div>
    <div class="text-center" style="margin-top: 10px">
      <a href="javascript:window.history.back();" class="btn btn-link">Back</a>
    </div>
    <div class="text-center" style="margin-top: 20px;">
      <h1><b>{{ song[0].name }}</b></h1>
      <audio controls :src="'/static/audio/' + song[0].name + '.mp3'" type="audio/mpeg" @error="audioError">
        Audio not available.
      </audio>
      <div v-if="role.includes('user')" class="mt-3">
        <button type="button" :class="{'btn btn-success': !is_liked, 'btn btn-secondary': is_liked}" @click="like(song[0].id)">Like</button>
        <button type="button" :class="{'btn btn-primary': !is_disliked, 'btn btn-secondary': is_disliked}" @click="dislike(song[0].id)">Dislike</button>
        <button type="button" class="btn btn-danger" @click="flag(song[0].id)" v-if="!flagged">Flag</button>
      </div>
      <div class="mt-3 text-center">
        <h5 style="white-space: pre-line;">{{ song[0].lyrics }}</h5>
      </div>
    </div>`,
    data() {
      return {
        role: localStorage.getItem('role'),
        token: localStorage.getItem('auth_token'),
        song: this.$route.query.song,
        is_liked: false,
        is_disliked: false,
        flagged: false,
      }
    },
    methods: {
        async like(song_id) {
          if (this.is_liked === false) {
            const response = await fetch(`/like_song/${song_id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': this.token,
              },
              body: JSON.stringify({ song_id: song_id }),
            });
      
            if (response.status === 200) {
              const response_data = await response.json();
              this.is_liked = true;
              this.is_disliked = false;
              alert(response_data.message);
            } else {
              const error = await response.json();
              alert(error.message);
            }
          } 
          else {
            alert('You have already liked this song');
          }

        },
      
        async dislike(song_id) {
          if (this.is_disliked === false) {
            const response = await fetch(`/dislike_song/${song_id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('auth_token'),
              },
              body: JSON.stringify({ song_id: song_id }),
            });
      
            if (response.status === 200) {
              const response_data = await response.json();
              this.is_disliked = true;
              this.is_liked = false;
              alert(response_data.message);
            } else {
              const error = await response.json();
              alert(error.message);
            }

          } 
          else {
            alert('You have already disliked this song');
          }

        },
        async flag(song_id){
          const confirm_flag = window.confirm("Are you sure you want to flag this song?")
          if (confirm_flag == true && this.flagged == false){
              const response = await fetch(`/flag_song/${song_id}`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                      'Authentication-Token': this.token,
                  },
              })
              if (response.status == 200) {
                  const response_data = await response.json();
                  alert(response_data.message);
                  this.flagged = true
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
      audioError() {
        alert('Audio not available right now.');
        this.$router.push('/user_dash');
      },
    }      
}