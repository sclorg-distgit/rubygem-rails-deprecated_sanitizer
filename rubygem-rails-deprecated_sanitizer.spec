%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from rails-deprecated_sanitizer-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rails-deprecated_sanitizer

# Tests require rails-dom-testing, which depends on rails-deprecated_sanitizer
%global bootstrap 1

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.0.3
Release: 5%{?dist}
Summary: Deprecated sanitizer API extracted from Action View
Group: Development/Languages
License: MIT
URL: https://github.com/rails/rails-deprecated_sanitizer
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(activesupport)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix}rubygem(activesupport)
%if 0%{bootstrap} < 1
BuildRequires: %{?scl_prefix}rubygem(actionview)
%endif
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
In Rails 4.2 HTML sanitization has been rewritten using a more secure library.

This gem includes the old behavior shipping with Rails 4.2 and before. It is
strictly provided to ease migration. It will be supported until Rails 5.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

# Relax AS dependency.
sed -i '/activesupport/ s/4.2.0/4.1.0/' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Run the test suite
%check
%if 0%{bootstrap} < 1
pushd .%{gem_instdir}
# Don't use Bundler.
sed -i "/require 'bundler\/setup'/ s/^/#/" test/test_helper.rb

# ActiveSupport::TestCase.test_order is not available in AS 4.1.
sed -i "/\.test_order/ s/^/#/" test/test_helper.rb

%{?scl:scl enable %{scl} - << \EOF}
ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
%{?scl:EOF}
popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/test

%changelog
* Sat Feb 20 2016 Pavel Valena <pvalena@redhat.com> - 1.0.3-5
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.3-2
- Relax ActiveSupport dependency.

* Tue Jan 20 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Initial package
