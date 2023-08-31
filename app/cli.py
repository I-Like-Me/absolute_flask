import time
from app import db
from app.library import product_levels
from app.models import User, App, Version
from app.main.absolute_api import Abs_Actions
from app.main.tool_box import Translators as Tlr, Library_Table_Dict_Builders as LTDB


def register(app):
    @app.cli.command()

    # Updates the version table.
    def update_version_table():
        """Update version table."""
        print('Starting process...')
        time.sleep(2)
        print('Getting version list...')
        citrix_versions = Abs_Actions.app_version_get(Tlr.app_select_tlr('Citrix')[0], Tlr.app_select_tlr('Citrix')[1])
        zoom_versions = Abs_Actions.app_version_get(Tlr.app_select_tlr('Zoom')[0], Tlr.app_select_tlr('Zoom')[1])
        citrix_ver_dict = LTDB.ctx_lib_tab_dict("Citrix", citrix_versions)
        zoom_ver_dict = LTDB.ctx_lib_tab_dict("Zoom", zoom_versions)
        citrix_add_count = 0
        zoom_add_count = 0
        windows_add_count = 0
        print('Adding versions...')
        time.sleep(2)
        ctx = App.query.filter_by(name="Citrix").first()
        for f, r in citrix_ver_dict.items():
            cur_fake_ver = Version.query.filter_by(fake_key=f).first()
            if cur_fake_ver is None:
                v = Version(fake_key=f, true_key=r, program=ctx)
                db.session.add(v)
                db.session.commit()
                citrix_add_count += 1
                ctx = App.query.filter_by(name="Citrix").first()
        zoom = App.query.filter_by(name="Zoom").first()
        for f, r in zoom_ver_dict.items():
            cur_fake_ver = Version.query.filter_by(fake_key=f).first()
            if cur_fake_ver is None:
                v = Version(fake_key=f, true_key=r, program=zoom)
                db.session.add(v)
                db.session.commit()
                zoom_add_count += 1
        windows = App.query.filter_by(name="Windows Product Level").first()
        for r, f in product_levels.items():
            cur_fake_ver = Version.query.filter_by(fake_key=f).first()
            if cur_fake_ver is None:
                v = Version(fake_key=f, true_key=r, program=windows)
                db.session.add(v)
                db.session.commit()
                windows_add_count += 1 
        if citrix_add_count != 0:
            print('Checking citrix for changes...')
            print(citrix_add_count)
            time.sleep(2)
        else:
            print('No new citrix versions to add.')
            time.sleep(2)
        if zoom_add_count != 0:
            print('Checking zoom for changes...')
            print(zoom_add_count)
            time.sleep(2)
        else:
            print('No new zoom versions to add.')
            time.sleep(2)
        if windows_add_count != 0:
            print('Checking windows for changes...')
            print(windows_add_count)
            time.sleep(2)
        else:
            print('No new windows versions to add.')
            time.sleep(2)
        print('Request_complete')

