#!/usr/bin/env python3
"""Colima Dashboard - Streamlit GUI for Colima VMs."""
import streamlit as st
import subprocess
import json
from datetime import datetime

COLIMA_BIN = "/opt/homebrew/bin/colima"

def run_cmd(cmd, timeout=120):
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
         )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except FileNotFoundError:
        return -1, "", "Command not found"

def run_colima(args, timeout=120):
    return run_cmd([COLIMA_BIN] + args, timeout)

def ssh_cmd(vm_name, command, timeout=30):
    cmd = f"ssh {vm_name} '{command}' 2>/dev/null"
    result = subprocess.run(
        cmd, shell=True, capture_output=True,
        text=True, timeout=timeout
     )
    return result.returncode, result.stdout, result.stderr

def get_vm_list():
    rc, stdout, stderr = run_colima(["list", "--json"])
    if rc != 0:
        return [{"type": "error", "message": stderr.strip()}]
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return [{"type": "error", "message": stdout.strip()}]

def main():
    st.set_page_config(
        page_title="Colima Dashboard",
        page_icon="🐋"
     )
    st.title("🐋 Colima Dashboard")
    st.caption("Manage your Colima VMs from a web browser.")

    with st.sidebar:
        st.header("Controls")
        if st.button("Refresh Status", type="primary", use_container_width=True):
            st.session_state["last_refresh"] = datetime.now()
        st.session_state.setdefault("last_refresh", datetime.now())
        st.caption(f"Refreshed: {st.session_state['last_refresh'].strftime('%H:%M:%S')}")

        st.divider()
        st.header("Help")
        st.markdown("""
- **Create VM**: Run `colima start` in terminal
- **SSH into VM**: Run `colima ssh` in terminal
- **Docker**: Run `docker run ...` inside the VM
        """)

    st.divider()
    st.header("VM Overview")

    vms = get_vm_list()

    error_only = (len(vms) == 1 and vms[0].get("type") == "error")
    if error_only or not vms:
        st.warning("No VMs found.")
        st.code("colima start\n# or:\ncolima start --cpu 4 --memory 8")
        return

    for vm in vms:
        if vm.get("type") == "error":
            st.error(f"Error: {vm['message']}")
            continue

        name = vm.get("name", "?")
        status = vm.get("status", "?").lower()
        arch = vm.get("arch", "?")
        cpus = vm.get("cpus", 0)
        memory = vm.get("memory", 0)
        disk = vm.get("disk", 0)

        status_map = {
            "running": ("✅", True, "Running"),
            "stopped": ("⏹️", False, "Stopped"),
            "paused": ("⏸️", False, "Paused"),
        }
        icon, running, label = status_map.get(status, (f"❓", False, status))

        col1, col2, col3 = st.columns([2, 1, 1])
        col1.markdown(f"**{icon} {name}**     `arch: {arch}`     `cpus: {cpus}`     `memory: {memory}G`")
        col2.markdown(f"Disk: **{disk} MB**")
        col3.metric("Status", label)

        b1, b2, b3 = st.columns(3)
        if running:
            with b1:
                if st.button(f"⏹ Stop", key=f"stop_{name}", use_container_width=True):
                    with st.spinner(f"Stopping {name}..."):
                        rc, out, err = run_colima(["stop", name])
                        if rc == 0:
                            st.success(f"`{name}` stopped!")
                        else:
                            st.error(f"Failed: {err}")
                    st.rerun()
            with b2:
                if st.button(f"🔄 Restart", key=f"re_{name}", use_container_width=True):
                    with st.spinner(f"Restarting {name}..."):
                        rc, out, err = run_colima(["restart", name])
                        if rc == 0:
                            st.success(f"`{name}` restarted!")
                        else:
                            st.error(f"Failed: {err}")
                    st.rerun()
            with b3:
                del_chk = st.checkbox(f"Delete", key=f"dchk_{name}")
                if del_chk and st.button(f"🗑 Delete", key=f"del_{name}", use_container_width=True):
                    with st.spinner(f"Deleting {name}..."):
                        rc, out, err = run_colima(["delete", name])
                        if rc == 0:
                            st.success(f"`{name}` deleted!")
                        else:
                            st.error(f"Failed: {err}")
                    st.rerun()
        else:
            with b1:
                if st.button(f"▶ Start", key=f"sta_{name}", use_container_width=True):
                    with st.spinner(f"Starting {name}..."):
                        rc, out, err = run_colima(["start", name])
                        if rc == 0:
                            st.success(f"`{name}` started!")
                        else:
                            st.error(f"Failed: {err}")
                    st.rerun()
            with b2:
                pass
            with b3:
                del_chk = st.checkbox(f"Delete", key=f"dchk2_{name}")
                if del_chk and st.button(f"🗑 Delete", key=f"del2_{name}", use_container_width=True):
                    with st.spinner(f"Deleting {name}..."):
                        rc, out, err = run_colima(["delete", name])
                        if rc == 0:
                            st.success(f"`{name}` deleted!")
                        else:
                            st.error(f"Failed: {err}")
                    st.rerun()

        st.divider()

    st.divider()
    st.header("Containers")
    for vm in vms:
        if vm.get("type") == "error" or vm.get("status", "").lower() != "running":
            continue
        name = vm.get("name", "?")
        st.markdown(f"### `{name}`")
        rc, stdout, stderr = ssh_cmd(name, "docker ps -a --format json")
        if rc != 0 or not stdout.strip():
            st.info("No containers. Start one with `docker run ...` in terminal.")
        else:
            containers = []
            for line in stdout.strip().split('\n'):
                if line:
                    try:
                        containers.append(json.loads(line))
                    except:
                        pass
            if containers:
                for c in containers:
                    st.json(c)
            else:
                st.info("No containers running.")

if __name__ == "__main__":
    main()
