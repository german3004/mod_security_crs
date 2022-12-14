Summary: ModSecurity Rules
Name: mod_security_crs
Version: 4.0.0
Release: 5%{?dist}
License: ASL 2.0
URL: https://coreruleset.org
Group: System Environment/Daemons
Source0: https://codeload.github.com/coreruleset/coreruleset/tar.gz/refs/tags/v4.0.0-rc1
Source1: https://github.com/german3004/mod_security_crs/raw/main/plugins/plugins.tar.gz 
Source2: https://raw.githubusercontent.com/german3004/mod_security_crs/main/plugins/tilsor_plugins-config.conf
BuildArch: noarch
Requires: mod_security >= 2.8.0
Obsoletes: mod_security_crs-extras < 3.0.0

%description
This package provides the base rules for mod_security.

%prep
#%setup -q -n coreruleset-%{version}
%setup -q -n coreruleset-%{version}-rc1

%build

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins-config
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins
install -d %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules
install -d %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins
install -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins/tilsor_plugins-config.conf 

# To exclude rules (pre/post)
mv rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
mv rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf

install -m0644 rules/* %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules/
mv crs-setup.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/crs-setup.conf

# activate base_rules
for f in `ls %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules/` ; do
    ln -s %{_datarootdir}/mod_modsecurity_crs/rules/$f %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/$f;
done

# activate all plugins
#install -Dp -m0644 %{SOURCE1} %{buildroot}%{_datarootdir}/plugins/plugins.tar.gz
tar -xzf %{SOURCE1} -C %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins/
#for f in `ls %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins/*/*-before.conf 2> /dev/null` ; do
for f in `find %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins/ -type f -name '*before*' -name '*.conf' 2> /dev/null` ; do
    #ln -s %{_datarootdir}/mod_modsecurity_crs/plugins/$(basename $f) %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins/$(basename $f);
    ln -s %{_datarootdir}/mod_modsecurity_crs/plugins/$(basename $(dirname $f))/$(basename $f) %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins/$(basename $f);
done
#for f in `ls %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins/*/*-after.conf 2> /dev/null` ; do
for f in `find %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins/ -type f -name '*after*' -name '*.conf' 2> /dev/null` ; do
    #ln -s %{_datarootdir}/mod_modsecurity_crs/plugins/$(basename $f) %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins/$(basename $f);
    ln -s %{_datarootdir}/mod_modsecurity_crs/plugins/$(basename $(dirname $f))/$(basename $f) %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins/$(basename $f);
done
#for f in `ls %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins/*/*-config.conf 2> /dev/null` ; do
for f in `find %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins/ -type f -name '*config*' -name '*.conf' 2> /dev/null` ; do
    #ln -s %{_datarootdir}/mod_modsecurity_crs/plugins/$(basename $f) %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins-config/$(basename $f);
    ln -s %{_datarootdir}/mod_modsecurity_crs/plugins/$(basename $(dirname $f))/$(basename $f) %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins-config/$(basename $f);
done

# There are some files that its names does not contains the word 'config', 'after' or 'before', for example antivirus.lua
for f in `find %{buildroot}%{_datarootdir}/mod_modsecurity_crs/plugins/ -type f -not -name '*config*' -not -name '*after*' -not -name '*before*' -not -name '*tar.gz' 2> /dev/null` ; do
    #ln -s %{_datarootdir}/mod_modsecurity_crs/plugins/$(basename $f) %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins/$(basename $f);
    ln -s %{_datarootdir}/mod_modsecurity_crs/plugins/$(basename $(dirname $f))/$(basename $f) %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/plugins/$(basename $f);
done

%files
%license LICENSE
%doc CHANGES README.md
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/activated_rules/*
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/plugins-config/*
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/plugins/*
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/crs-setup.conf
%{_datarootdir}/mod_modsecurity_crs



%changelog
* Mon Aug 30 2021 Rodrigo Martinez <rmartinez@tilsor.com.uy> - 3.3.2
- Update to last version for bug in Drupal rules in branch 3.3

* Tue Jul 13 2021 Rodrigo Martinez <rmartinez@tilsor.com.uy> - 3.1.2
- Update to last version for bug in Drupal rules

* Wed Nov 06 2019 Mario del Riego <mdelriego@tilsor.com.uy> - 3.2.0
- Update to final release

* Thu Dec 13 2018 <mdelriego@tilsor.com.uy> - 3.1.0
- Update to final release

* Tue Sep 11 2018 <fzipitria@tilsor.com.uy> - 3.1.0-RC1
- Update to release candidate

