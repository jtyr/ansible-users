users
=====

Ansible role which helps to create and manage Linux users, groups and SSH keys.

The configuration of the role is done in such way that it should not be
necessary to change the role for any kind of configuration. All can be
done either by changing role parameters or by declaring completely new
configuration as a variable. That makes this role absolutely
universal. See the examples below for more details.

Please report any issues or send PR.


Examples
--------

```yaml
---

- name: Example of how to create a group
  hosts: all
  vars:
    users:
      - group: testgroup
  roles:
    - users

- name: Example of how to remove a group
  hosts: all
  vars:
    users:
      - group: testgroup
        group_state: absent
  roles:
    - users

- name: Example of how to create a user
  hosts: all
  vars:
    users:
      - name: myuser
  roles:
    - users

- name: Example of how to remove a user
  hosts: all
  vars:
    users:
      - name: myuser
        state: absent
  roles:
    - users

- name: Example of how to create a user with a specific UID, group and GID, comment, password and SSH public key
  hosts: all
  vars:
    users:
      - name: myuser
        uid: 2000
        group: myusers
        gid: 2000
        comment: My user
        password: "$6$DaWdfn9ZmxeMMMe/$3snNH112PneNfs81JGCD4p5f10b7gnNgF8wk.2HPp0ZzWrxrPnH66YE4PDN.WP11X618U47eEX2Mr2cSv4ec61"
        ssh_keys:
          - ssh-rsa AAAAB3NzaC1yc2EAAAEDAQABAAABAQCWp73FFB8Ck/S6i3lTijbfQGxnHC84iu7anCfSeyJE89JuI9C2OU+QlW6tsl/SbXY2LR0TGUhD5aX2ZvC3CZrrl4Yq4/9upEVgUpzJdDJo6ZcLOWVDuetHArNbIC2pcdU/skDoCP0wcuBJ09qLZ4qi5q/r6RS79PmzhvNg6CjzmT5wztMZIjlS4Z7+RqeR1WZMur8FXRfy25jqewdUUWIDVxOvRJLvwB1tW9NA9oe7jp4E9FAn4ZgsMs/143N8bw16M5g7c6nOMvQUBRld10ZnO10QTMpE3WWKiHgyCeQCdZ8W4EsrIUelbOoLkFuMADoZ9gO9biJ/2aKIqr9n+++d ansible@host
  roles:
    - users

- name: Example of how to create a SFTP user
  hosts: all
  vars:
    users:
      - name: myuser
        group: sftp
        home: /sftp/myuser
        # The user doesn't need shell
        shell: /bin/false
        # Explicite list of allowed public SSH keys
        ssh_keys:
          - ssh-rsa AAAAB3NzaC1yc2EAAAEDAQABAAABAQCWp73FFB8Ck/S6i3lTijbfQGxnHC84iu7anCfSeyJE89JuI9C2OU+QlW6tsl/SbXY2LR0TGUhD5aX2ZvC3CZrrl4Yq4/9upEVgUpzJdDJo6ZcLOWVDuetHArNbIC2pcdU/skDoCP0wcuBJ09qLZ4qi5q/r6RS79PmzhvNg6CjzmT5wztMZIjlS4Z7+RqeR1WZMur8FXRfy25jqewdUUWIDVxOvRJLvwB1tW9NA9oe7jp4E9FAn4ZgsMs/143N8bw16M5g7c6nOMvQUBRld10ZnO10QTMpE3WWKiHgyCeQCdZ8W4EsrIUelbOoLkFuMADoZ9gO9biJ/2aKIqr9n+++d ansible@host
        # The home directory is writable only by root
        # (user cannot create any files or directories there)
        home_mode: "0755"
        home_owner: root
        home_group: root
        # The ~/.ssh directory is also writable only by root (user cannot delete it),
        # but sftp group can read from it
        ssh_dir_mode: "0710"
        ssh_dir_owner: root
        ssh_dir_group: sftp
        # The authorized_keys file is readable by the sftp group
        # (user cannot edit it)
        ssh_auth_mode: "0640"
        ssh_auth_owner: root
        ssh_auth_group: sftp
        # We can restrict the home directory creation to a specific host
        # (usefull when the home directory is created on a shared storage)
        host: gluster-centos7a
        # Create ~/data directory which is writable by the sftp group
        # (owned by root to prevent its deletion by the user)
        add_dirs:
          - name: data
            owner: root
            group: sftp
            mode: "0770"
  roles:
    - users

- name: Example of a more complex user management
  hosts: all
  vars:
    # Salt for always the same password hash
    users_password_salt: mysecretsalt

    # To facilitate simple password change
    users_root_password: "{{ 'ro0t123' | password_hash('sha512', users_password_salt) }}"
    users_ansible_password: "{{ 'ans1bl3' | password_hash('sha512', users_password_salt) }}"

    # Default list of users
    users__default:
      # Set root password
      - name: root
        password: "{{ users_root_password }}"
      # Create ansible user and group
      - name: ansible
        uid: 1000
        group: ansible
        gid: 1000
        comment: Configuration management user
        password: "{{ users_ansible_password }}"
        # Add single SSH public key
        ssh_keys:
          - ssh-rsa AAAAB3NzaC1yc2EAAAEDAQABAAABAQCWp73FFB8Ck/S6i3lTijbfQGxnHC84iu7anCfSeyJE89JuI9C2OU+QlW6tsl/SbXY2LR0TGUhD5aX2ZvC3CZrrl4Yq4/9upEVgUpzJdDJo6ZcLOWVDuetHArNbIC2pcdU/skDoCP0wcuBJ09qLZ4qi5q/r6RS79PmzhvNg6CjzmT5wztMZIjlS4Z7+RqeR1WZMur8FXRfy25jqewdUUWIDVxOvRJLvwB1tW9NA9oe7jp4E9FAn4ZgsMs/143N8bw16M5g7c6nOMvQUBRld10ZnO10QTMpE3WWKiHgyCeQCdZ8W4EsrIUelbOoLkFuMADoZ9gO9biJ/2aKIqr9n+++d ansible@host

    # Custom list of users
    users__custom:
      # Existing remote user (e.g. from LDAP)
      - remote: yes
        name: service1
        # Add multiple SSH public keys
        ssh_keys:
          - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAEABAQCWp73FFB8Ck/S6i6lTjibfQGxnHC84iu7anCfSeyJE89JuI9C2OU+QlWatsl/SbXY2LR0TGUhD5aX2ZvC3CZrrl4Yq4/fy25jqewdUUWIDVxOvRJLvwB1tW9NA9oe7jp9upEVgUpzJdDJo6ZcLOWVDuetHArNbIC2pcdU/skcoCP0wcuBJ09qLZ4qi5q/r6RS79PmzhvNg6CjzmT5wztMZIjlS4Z7+RqeR8WZMur8FXR4E9FAn4ZgsMs/143N8bw16M5g7c6nOMvQUBRld10ZnO10QtMpE3WWKiHgyCeQCdZ8W4EsrIUelbOoLkFuMADoZ9gO9biJ/2aKIqr9n+++d ansible@host1
          - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABACABAQCWp73FFB8Ck//skcoEP0wcuBJ09qLZ4qi5q/r6RS79PmzhvNg6CjzmT5wzt3ZIjlS4Z7+RqeR8WZMur8FXRfy25jqewdUUWIDVxOvRJLvwB1tW9NA9oe7jp4E9FAn4ZgsMs/143N8bw16M5g7c6nOMvQUBRld10ZnO10QTMpE3WWKiHgyCeQCdZ8W4EsrIUelbOoLkFuMADoZ9gO9biJS6i6lTijbfQGxnHC84iu7anCfSeyJE89JuI9C2OU+QlW6tsl/SbXY2LR0TGUhD5aX2ZvC3CZrll4Yq4/9upEVgUpzJdDJo6ZcLOWVDuetHArNbIC2pcdU/2aKIqr9n+++d ansible@host2
      # Remove previously created user
      - name: johndoe
        comment: John Doe
        group: users
        state: absent
        password: "{{ users_ansible_password }}"

    # Final list of users
    users: "{{
      users__default +
      users__custom }}"
  roles:
    - users
```


Role variables
--------------

```yaml
# Whether to remove the user's home directory when the `state` set to `absent`
users_remove: yes

# Add SSH keys exclusively (remove all unknown keys)
users_ssh_keys_exclusive: yes

# List of users/groups to be created (see README for examples)
users: []
```


License
-------

MIT


Author
------

Jiri Tyr
