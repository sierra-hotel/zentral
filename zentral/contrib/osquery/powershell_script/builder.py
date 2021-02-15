import os
from django.http import HttpResponse
from zentral.utils.osx_package import APIConfigToolsMixin
from zentral.contrib.osquery.forms import EnrollmentForm


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class OsqueryZentralEnrollPowershellScriptBuilder(APIConfigToolsMixin):
    form = EnrollmentForm
    script_name = "zentral_osquery_setup.ps1"

    def __init__(self, enrollment):
        self.business_unit = enrollment.secret.get_api_enrollment_business_unit()
        self.build_kwargs = {
            "enrollment_secret_secret": enrollment.secret.secret,
            "release": enrollment.osquery_release,
            "serialized_flags": enrollment.configuration.get_serialized_flags(),
        }

    def build_and_make_response(self):
        template_path = os.path.join(BASE_DIR, "template.ps1")
        with open(template_path, "r") as f:
            content = f.read()

        # tls hostname
        tls_hostname = self.get_tls_hostname()
        content = content.replace("%TLS_HOSTNAME%", tls_hostname)

        serialized_flags = self.build_kwargs["serialized_flags"]

        # tls server certs
        tls_fullchain = self.get_tls_fullchain()
        if tls_fullchain:
            content = content.replace("%INCLUDE_TLS_SERVER_CERTS%", "1")
            tls_server_certs_file = f"C:\\Program files\\osquery\\certs\\{tls_hostname}.pem"
            content = content.replace("%TLS_SERVER_CERTS_FILE%", tls_server_certs_file)
            content = content.replace("%TLS_SERVER_CERTS%", tls_fullchain)
            serialized_flags.append(
                "--tls_server_certs='{}'".format(tls_server_certs_file)
            )
        else:
            content = content.replace("%INCLUDE_TLS_SERVER_CERTS%", "0")

        # enrollment secret
        content = content.replace("%ENROLL_SECRET_SECRET%", self.build_kwargs["enrollment_secret_secret"])

        # extra flags
        content = content.replace("%EXTRA_FLAGS%", "\n".join(serialized_flags))

        # only config or install + config
        # TODO: we can't pin it to a known osquery version if we configure the repos
        # not really coherent with the form
        release = self.build_kwargs.get("release")
        install_osquery = release > ""
        content = content.replace("%INSTALL_OSQUERY%", str(int(install_osquery)))
        content = content.replace("%OSQUERY_RELEASE%", release.replace(".pkg", ".msi"))

        # convert newlines
        content = content.replace("\n", "\r\n")

        response = HttpResponse(content, "text/plain")
        response['Content-Length'] = len(content)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.script_name)
        return response
