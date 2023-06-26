export function get_reels(set_reels) {
    fetch("/reels").then(
      res => res.json()
    ).then(
      data => {
        set_reels(data)
        console.log(data)
      }
    )
}

export function get_balance(set_balance){
    fetch("/get_balance").then(
        res => res.json()
    ).then(
        data=> {
            set_balance(data)
            console.log(data)
        }
    )
}

export function reshuffle() {
    return fetch('/reshuffle', { method: 'POST' })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log('Reshuffle was successful');
          return data.success;
        } else {
          console.log('Reshuffle failed');
          return false;
        }
      })
      .catch((error) => {
        console.log('Network error: ', error);
        return false;
      });
}
