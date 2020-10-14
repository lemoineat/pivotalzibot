Trackerzibot is a
[Pivotal Tracker](https://www.pivotaltracker.com/) bot that mirrors
changes made on [Pivotal Tracker](https://www.pivotaltracker.com/) to  [Bugzilla](https://www.bugzilla.org/). It works better with the [trackerzilla](https://github.com/lemoineat/Trackerzilla/) extention for Bugzilla.

### Install

On need python3 installed on your server. Install the dependencies with `pip3 install -r requirements.txt`
Then modifies the `config.py` file. `BUGZILLA_ADDR` is the address of your bugzilla server.
`API_KEY` is a key generated in the "preference -> API Key" panel of bugzilla.

## nginx

Replace the DOMAINE_NAME occurences (for instance my.cool.domain.name.com) in `trackerzibot_nginx`, move `trackerzibot_nginx` in `/etc/nginx/sites-available/`, run `ln -s /etc/nginx/sites-available/trackerzibot_nginx /etc/nginx/sites-enabled/trackerzibot_nginx`, check the config with `nginx -t` (you may need to comment the lines begining by ssl first), then run `systemctl restart nginx` to load your config. Run `sudo certbot certonly --webroot -w /usr/local/share/trackerzibot/ -d DOMAINE_NAME` (replace DOMAINE_NAME) to get the ssl certificat. If you commented the ssl lines, uncomment them and rerun `nginx -t` and `systemctl restart nginx`.


## supervisord

If you use supervisord you can put the repository in `/usr/local/share/`,  and move `trackerzibot.conf` in `/etc/supervisor/conf.d/`, then run `supervisorctl reread`, then `supervisorctl update` to update supervisor. You can check if it works with `supervisorctl status`.

(currently `supervisorctl stop` cant kill the bot, you can use `sudo pkill gunicorn`)


### Story title

Your story must be named `Bug 42: my story` where 42 is id off the bug on Bugzilla.

### Commments

You can send a comment to Bugzilla from a well named story by adding `@bugs` in the comment.

### Status update

If your story is well named, the status changes are mirrored to the Bugzilla bug. The mapping Pivotal status -> Bugzilla status can be change in the `config.py` file (STATUS_PIVOTAL_TO_BUGZILLA).
