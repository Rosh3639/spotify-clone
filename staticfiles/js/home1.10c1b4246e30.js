
const player = document.querySelector('.audio-player')
const play = document.querySelector('.playing')
const prev = document.querySelector('.prev')
const next = document.querySelector('.next')
const currentTime = document.querySelector('.currentDuration')
const duration = document.querySelector('.Duration')
const progress = document.querySelector('.progress')
const progress_container = document.querySelector('.progress_container')
const audio_tracks = document.querySelector('.audio-tracks')
const song_title = document.querySelector('.song-title')
const artist = document.querySelector('.artist')
const album = document.querySelector('.album')
const music_img = document.querySelector('.music_img')

// initilize music indexing
let musicIndex = 0

//get music document from backend 
const musics = JSON.parse(document.getElementById('musics').textContent)


// functions
// format time for music
const formatTime = secs => {
    let min = Math.floor((secs % 3600) / 60);
    let sec = Math.floor(secs % 60)
    if (sec < 10) {
        sec = `0${sec}`
    }

    return `${min}:${sec}`
}

// loading a set detail of music in UI
const setSRC = () => {

    player.src = `/media/${musics[musicIndex].audio_file}`
    song_title.textContent = musics[musicIndex].title
    artist.textContent = musics[musicIndex].artiste
    music_img.setAttribute('src', `media/${musics[musicIndex].cover_image}`)
    if (musics[musicIndex].album_id !== null) {
        album.textContent = musics[musicIndex].album_id
    } else {
        album.textContent = 'Single'

    }

}

//determine player should play or not 
const playOrPause = () => {
    if (player.paused) {
        player.play()

    } else {
        player.pause()

    }
}

// load first music
setSRC()
player.pause()

// eventlisteners
// when play btn is clicked
play.addEventListener("click", e => {

    playOrPause()
})

// update the progress bar
player.addEventListener('timeupdate', e => {
    let secs = player.currentTime
    let total = player.duration

    currentTime.textContent = formatTime(player.currentTime)

    let progress_container_width = progress_container.offsetWidth
    let progress_width = progress.offsetWidth

    let audio_played = (secs / total) * 100
    let newWidth = progress_container_width * (audio_played / 100)

    progress.style.width = `${newWidth}px`

})

//when a progress bar is clicked to change music timer 
progress_container.addEventListener('click', (e) => {
    const click_percentage = (e.offsetX / progress_container.offsetWidth) * 100
    // console.log(click_percentage)
    const audio_played = (click_percentage / 100) * player.duration
    // console.log(audio_played)
    let plaing
    if (player.paused) {
        playing = false
    } else {
        playing = true
    }
    player.currentTime = audio_played

    if (playing == false) {
        player.pause()
    }


})

// loads durations of music for current music to UI
player.addEventListener('loadedmetadata', () => {
    duration.textContent = formatTime(player.duration)
    // console.log(duration.textContent)
})

// when an audio is chosen from the song tracks
audio_tracks.addEventListener('click', e => {
    if ((e.target.nodeName == 'BUTTON' && e.target.classList.contains('play_single')) ||
        (e.target.nodeName == 'svg' && e.target.classList.contains('play_svg'))) {
        let parent_cont

        if (e.target.nodeName == 'BUTTON') {
            parent_cont = e.target.parentNode
        } else {
            parent_cont = e.target.parentNode.parentNode
        }
        const newIndex = Array.from(audio_tracks.querySelectorAll('li')).indexOf(
            parent_cont)

        if (newIndex == musicIndex) {
            if (player.paused) {

                player.play()
            } else {

                player.pause()
            }
        } else {

            musicIndex = newIndex
            setSRC()
            player.play()
        }

    }
})

// when the prev btn is clicked
prev.addEventListener('click', () => {
    musicIndex = musicIndex - 1
    if (musicIndex < 0) {
        musicIndex = musics.length - 1
    }

    setSRC()

    playOrPause()
})

// when the next btn is clicked
next.addEventListener('click', () => {
    musicIndex = musicIndex + 1

    if (musicIndex > musics.length - 1) {
        musicIndex = 0
    }

    setSRC()

    playOrPause()

})
