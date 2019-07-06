cred = 'cred.txt'
lildisksprefix = '/mnt/disk'
bigdisk = '/mnt/bigdisk'
forever = '2fstab.sh'
cleansh = 'clean.sh'
once = 'first.sh'

with open(cred) as f:
    creds = [i.split(':') for i in f.read().split('\n') if (not i == '' and not i[0]=='#')]
with open(once, 'w') as w:
    w.write('backup/backup.sh\n')
    folds = []
    for index,acc in enumerate(creds):
        fold = '%s%d'%(lildisksprefix,index)
        folds.append(fold)
        w.write('mkdir %s\n'%fold)
        w.write('echo %s %s %s >> /etc/davfs2/secrets\n'%(fold, *acc))
        w.write('mount -t davfs https://webdav.yandex.ru %s\n'%fold)
    w.write('mkdir %s\n'%bigdisk)
    w.write('mhddfs %s %s -o default_permissions,allow_other\n'%(','.join(folds), bigdisk))
    
with open(forever, 'w') as w:
    for fold in folds:
        w.write('echo https://webdav.yandex.ru %s davfs user,_netdev,uid=username,file_mode=600,dir_mode=700 0 1 >> /etc/fstab\n'%fold)
    w.write('echo mhddfs#%s %s fuse default_permissions,allow_other 0 0 >> /etc/fstab\n'%(','.join(folds), bigdisk))

with open(cleansh, 'w') as w:
    w.write('umount %s\n'%bigdisk)
    for fold in folds:
        w.write('umount %s\n'%fold)
    w.write('backup/restore.sh\n')




print('\nDo:')
print('    apt install davfs2 mhddfs')
print("    chmod +x *.sh backup/*.sh")
print('')
print(forever, '- mount on startup')
print(cleansh, '- umount and remove from fstab and davfs2/secrets')
print(once, '- mount until reboot')