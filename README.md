CloudForms Python Client 
========================

Usage
-----

```
>>> import cloudformscli 
>>> cf_cli = cloudformscli.Client("https://<cf host>/api", "admin", "smartvm")
>>> cf_cli = cloudformscli.Client("https://localhost:8443/api", "admin", "smartvm")
>>> vm_mngr = cf_cli.vms
```

Get all VMs -
```
>>> vm_mngr.get_all()
...
```

Get all VMs expanding VM details -
```
>>> vm_mngr.get_all(expand=True)
...
```

Get VM by name -
```
>>> vm_mngr.get_by_name('globnpolvmm01')
...
```

Get VM by ID -
```
>>> vm_mngr.get_by_id('globnpolvmm01')
...
```

### Generic Objects

#### Generic Object Definition

```
>>> go_def_mngr = cf_cli.gen_obj_defs
>>> go_def_mngr.get_all()
...
>>> go_def_mngr.get_by_name('Network')
...
```

#### Generic Object

All generic objects manager across all gen obj definition types -
```
>>> go_mngr = cf_cli.gen_objects()
>>> go_mngr.get_all()
...
>>> go_mngr.get_all(expand=True)
...
>>> go_mngr.get_by_name('network-frontend')
...
>>> go_mngr.get_by_id('301000000000247')
...

Generic Object manager for a specific definition type -
```
>>> nw_go_mngr = cf_cli.gen_objects('Network')
```
Get all gen objects of 'Network' definition type -
```
>>> nw_go_mngr.get_all()
```

### Sending Actions

Send _start_ action to VM with the specified Id -
```
>>> vm_mngr.action('301000000000123', 'start')
```
