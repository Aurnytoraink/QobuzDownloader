python = import('python')
python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('pythondir', join_paths(get_option('prefix'), python3.sysconfig_path('purelib')))

configure_file(
  input: 'qobuzdownloader.in',
  output: 'qobuzdownloader',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

install_subdir('qobuzdownloader', install_dir: join_paths(get_option('prefix'), python3.sysconfig_path('purelib')))