# XMBSMDSJ V2.0

## Configurations
- SSL: place key and cert_chain in /cert directory
- Data files
```
/data
├── db
│   ├── db.sqlite3
│   └── media
└── media
    ├── blog
    ├── default
    ├── gallery
    └── images
```

# Deploy

```sh
sudo docker-compose up
```

## Updated 2019/11/29
- Migrated the stack from apache to nginx
- New docker configurations build the application from scrach, there's no need for a pre-built image for SSL purpose